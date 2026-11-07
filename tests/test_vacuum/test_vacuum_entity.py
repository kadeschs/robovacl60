"""Tests for the L60 vacuum entity: state mapping, attributes, restore and polling."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.components.vacuum import VacuumActivity
from homeassistant.core import State

from custom_components.robovacl60.tuyalocalapi import TuyaException
from custom_components.robovacl60.vacuum import UPDATE_RETRIES, RoboVacEntity

NO_ERROR_177 = "DAich8KqlJbzzgFSAA=="  # real L60 payload: no error codes
ERROR_2_177 = "BAgAEAI="  # length 4: field 1 = 0, field 2 = error code 2


@pytest.fixture
def entity(mock_robovac, mock_vacuum_data):
    with patch("custom_components.robovacl60.vacuum.RoboVac", return_value=mock_robovac):
        yield RoboVacEntity(mock_vacuum_data)


def push(entity: RoboVacEntity, dps: dict) -> None:
    """Simulate DPS arriving from the device (GET reply or gratuitous push)."""
    entity.vacuum._dps.update(dps)
    entity.update_entity_values()


def test_entity_setup(entity, mock_robovac):
    assert entity.unique_id == "test_l60_id"
    assert entity.fan_speed_list == ["Quiet", "Standard", "Turbo", "Max", "Boost_IQ"]
    assert entity.supported_features == mock_robovac.getHomeAssistantFeatures.return_value


@pytest.mark.parametrize(
    ("status_raw", "expected"),
    [
        ("BgoAEAUyAA==", VacuumActivity.CLEANING),
        ("CAoAEAUyAggB", VacuumActivity.PAUSED),
        ("BBAHQgA=", VacuumActivity.RETURNING),
        ("BBADGgA=", VacuumActivity.DOCKED),
        ("AhAB", VacuumActivity.DOCKED),
    ],
)
def test_activity_from_status(entity, status_raw, expected):
    push(entity, {"153": status_raw})
    assert entity.activity == expected
    assert entity.extra_state_attributes["status_raw"] == status_raw


def test_activity_unrecognised_status_is_idle(entity):
    push(entity, {"153": "zzzz"})
    assert entity.activity == VacuumActivity.IDLE


def test_missing_status_reports_idle_and_unknown(entity):
    """The L60's GET reply never carries 153, so a fresh cache has no status."""
    push(entity, {"158": "Max", "163": 100})
    assert entity.activity == VacuumActivity.IDLE
    attrs = entity.extra_state_attributes
    assert attrs["status"] == "Unknown"
    assert attrs["status_raw"] == "Unavailable"


def test_no_error_payload_before_status_is_not_an_error(entity):
    """Regression: 177 arrives ~250 ms before 153 at run start; it carries no codes."""
    push(entity, {"177": NO_ERROR_177})
    assert entity.activity == VacuumActivity.IDLE
    assert entity.extra_state_attributes["error"] == "None"
    push(entity, {"153": "BgoAEAUyAA=="})
    assert entity.activity == VacuumActivity.CLEANING


def test_real_error_without_status_is_error(entity):
    push(entity, {"177": ERROR_2_177})
    assert entity.activity == VacuumActivity.ERROR
    assert entity.extra_state_attributes["error"] == "error_2"


def test_real_error_does_not_override_known_status(entity):
    push(entity, {"153": "BgoAEAUyAA==", "177": ERROR_2_177})
    assert entity.activity == VacuumActivity.CLEANING


def test_connection_failed_is_idle(entity):
    entity.error_code = "CONNECTION_FAILED"
    assert entity.activity == VacuumActivity.IDLE


def test_dnd_and_boost_iq_attributes(entity):
    """Regression: 157/159 were read with int keys and never populated."""
    push(entity, {"157": False, "159": True, "158": "Max"})
    attrs = entity.extra_state_attributes
    assert attrs["do_not_disturb"] == "False"
    assert attrs["boost_iq"] == "True"
    assert attrs["fan_speed"] == "Max"


@pytest.mark.parametrize(
    ("raw", "shown"),
    [("Quiet", "Pure"), ("Boost_IQ", "Boost IQ"), ("Turbo", "Turbo")],
)
def test_fan_speed_display(entity, raw, shown):
    push(entity, {"158": raw})
    assert entity.fan_speed == shown


def test_mode_decoding(entity):
    push(entity, {"152": "AggG"})
    attrs = entity.extra_state_attributes
    assert attrs["mode"] == "home"
    assert attrs["mode_raw"] == "AggG"


async def _added_with_last_state(entity, last_state):
    with (
        patch(
            "homeassistant.helpers.restore_state.RestoreEntity.async_added_to_hass",
            AsyncMock(),
        ),
        patch.object(entity, "async_get_last_state", AsyncMock(return_value=last_state)),
    ):
        await entity.async_added_to_hass()


async def test_restore_docked_status(entity):
    await _added_with_last_state(
        entity, State("vacuum.basement", "docked", {"status_raw": "BBADGgA="})
    )
    assert entity.vacuum._dps["153"] == "BBADGgA="
    assert entity.activity == VacuumActivity.DOCKED


@pytest.mark.parametrize("status_raw", ["BgoAEAUyAA==", "Unavailable", None])
async def test_restore_skips_non_docked(entity, status_raw):
    await _added_with_last_state(
        entity, State("vacuum.basement", "cleaning", {"status_raw": status_raw})
    )
    assert "153" not in entity.vacuum._dps
    assert entity.activity == VacuumActivity.IDLE


async def test_restore_never_overwrites_live_status(entity):
    entity.vacuum._dps["153"] = "BgoAEAUyAA=="
    await _added_with_last_state(
        entity, State("vacuum.basement", "docked", {"status_raw": "BBADGgA="})
    )
    assert entity.vacuum._dps["153"] == "BgoAEAUyAA=="


async def test_restore_without_last_state(entity):
    await _added_with_last_state(entity, None)
    assert "153" not in entity.vacuum._dps


async def test_async_update_success(entity, mock_robovac):
    mock_robovac._dps.update({"163": 80, "158": "Turbo"})
    entity.update_failures = 2
    await entity.async_update()
    mock_robovac.async_get.assert_awaited_once()
    assert entity.update_failures == 0
    assert entity.fan_speed == "Turbo"


async def test_async_update_failures_force_reconnect(entity, mock_robovac):
    mock_robovac.async_get.side_effect = TuyaException("timeout")
    for _ in range(UPDATE_RETRIES):
        await entity.async_update()
    assert entity.update_failures == UPDATE_RETRIES
    assert entity.error_code == "CONNECTION_FAILED"
    assert entity.activity == VacuumActivity.IDLE
    mock_robovac.async_disconnect.assert_awaited_once()


async def test_will_remove_disables_device(entity, mock_robovac):
    await entity.async_will_remove_from_hass()
    mock_robovac.async_disable.assert_awaited_once()
