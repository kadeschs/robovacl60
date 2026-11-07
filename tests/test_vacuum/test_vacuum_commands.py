"""Tests for the commands the L60 entity sends to the device."""

from unittest.mock import patch

import pytest

from custom_components.robovacl60.vacuum import RoboVacEntity


@pytest.fixture
def entity(mock_robovac, mock_vacuum_data):
    with patch("custom_components.robovacl60.vacuum.RoboVac", return_value=mock_robovac):
        yield RoboVacEntity(mock_vacuum_data)


async def test_start(entity, mock_robovac):
    await entity.async_start()
    mock_robovac.async_set.assert_awaited_once_with({"152": "BBoCCAE="})


@pytest.mark.parametrize("method", ["async_pause", "async_stop"])
async def test_pause_and_stop(entity, mock_robovac, method):
    await getattr(entity, method)()
    mock_robovac.async_set.assert_awaited_once_with({"152": "AggN"})


async def test_return_to_base(entity, mock_robovac):
    await entity.async_return_to_base()
    mock_robovac.async_set.assert_awaited_once_with({"152": "AggG"})


async def test_clean_spot(entity, mock_robovac):
    await entity.async_clean_spot()
    mock_robovac.async_set.assert_awaited_once_with({"152": "AA=="})


@pytest.mark.parametrize(
    ("requested", "sent"),
    [
        ("Max", "Max"),
        ("Standard", "Standard"),
        ("Turbo", "Turbo"),
        ("Quiet", "Quiet"),
        ("Pure", "Quiet"),  # the label the entity displays for Quiet
        ("Boost IQ", "Boost_IQ"),
        ("Boost_IQ", "Boost_IQ"),
    ],
)
async def test_set_fan_speed(entity, mock_robovac, requested, sent):
    await entity.async_set_fan_speed(requested)
    mock_robovac.async_set.assert_awaited_once_with({"158": sent})


async def test_set_fan_speed_unsupported(entity, mock_robovac):
    await entity.async_set_fan_speed("No Suction")
    mock_robovac.async_set.assert_not_awaited()


@pytest.mark.parametrize(("current", "sent"), [(None, True), (False, True), (True, False)])
async def test_locate_toggles(entity, mock_robovac, current, sent):
    """Regression: 160 was read with an int key, so locate never switched off."""
    if current is not None:
        mock_robovac._dps["160"] = current
        entity.update_entity_values()
    await entity.async_locate()
    mock_robovac.async_set.assert_awaited_once_with({"160": sent})


async def test_send_command_auto_clean(entity, mock_robovac):
    await entity.async_send_command("autoClean")
    mock_robovac.async_set.assert_awaited_once_with({"152": "BBoCCAE="})


@pytest.mark.parametrize(
    ("command", "dps", "current", "sent"),
    [
        ("doNotDisturb", "157", False, True),
        ("doNotDisturb", "157", True, False),
        ("boostIQ", "159", False, True),
        ("boostIQ", "159", True, False),
    ],
)
async def test_send_command_toggles(entity, mock_robovac, command, dps, current, sent):
    mock_robovac._dps[dps] = current
    entity.update_entity_values()
    await entity.async_send_command(command)
    mock_robovac.async_set.assert_awaited_once_with({dps: sent})


@pytest.mark.parametrize(
    "command", ["edgeClean", "smallRoomClean", "autoReturn", "roomClean", "bogus"]
)
async def test_send_command_unsupported(entity, mock_robovac, command, caplog):
    await entity.async_send_command(command, {"roomIds": [1]})
    mock_robovac.async_set.assert_not_awaited()
    assert "not supported on the L60" in caplog.text


@pytest.mark.parametrize(
    "method",
    ["async_start", "async_pause", "async_stop", "async_return_to_base", "async_locate"],
)
async def test_commands_without_device(entity, method):
    entity.vacuum = None
    await getattr(entity, method)()  # logs an error, must not raise
