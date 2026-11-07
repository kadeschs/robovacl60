"""Tests for the RoboVac model wrapper with the T2267 (L60) model details."""

import pytest
from homeassistant.components.vacuum import VacuumEntityFeature

from custom_components.robovacl60.robovac import ModelNotSupportedException, RoboVac
from custom_components.robovacl60.vacuums import ROBOVAC_MODELS
from custom_components.robovacl60.vacuums.base import (
    RobovacCommand,
    RoboVacEntityFeature,
    TuyaCodes,
)
from tests.conftest import t2267_model


def test_only_t2267_is_registered():
    """The fork supports the L60 (T2267) only."""
    assert list(ROBOVAC_MODELS) == ["T2267"]


def test_unsupported_model_raises():
    """Any other model is rejected before a connection is attempted."""
    with pytest.raises(ModelNotSupportedException):
        RoboVac(model_code="T2118", device_id="x", host="h", local_key="0" * 16)


def test_home_assistant_features():
    features = t2267_model().getHomeAssistantFeatures()
    for flag in (
        VacuumEntityFeature.FAN_SPEED,
        VacuumEntityFeature.LOCATE,
        VacuumEntityFeature.PAUSE,
        VacuumEntityFeature.RETURN_HOME,
        VacuumEntityFeature.SEND_COMMAND,
        VacuumEntityFeature.START,
        VacuumEntityFeature.STATE,
        VacuumEntityFeature.STOP,
    ):
        assert features & flag


def test_robovac_features():
    features = t2267_model().getRoboVacFeatures()
    assert features & RoboVacEntityFeature.DO_NOT_DISTURB
    assert features & RoboVacEntityFeature.BOOST_IQ
    assert not features & RoboVacEntityFeature.CONSUMABLES


def test_fan_speeds():
    assert t2267_model().getFanSpeeds() == ["Quiet", "Standard", "Turbo", "Max", "Boost_IQ"]


def test_dps_codes_match_tuya_codes():
    """getDpsCodes() and TuyaCodes agree on every L60 DPS."""
    codes = t2267_model().getDpsCodes()
    assert codes["MODE"] == TuyaCodes.MODE == "152"
    assert codes["STATUS"] == TuyaCodes.STATUS == "153"
    assert codes["FAN_SPEED"] == TuyaCodes.FAN_SPEED == "158"
    assert codes["LOCATE"] == TuyaCodes.LOCATE == "160"
    assert codes["BATTERY_LEVEL"] == TuyaCodes.BATTERY_LEVEL == "163"
    assert codes["ERROR_CODE"] == TuyaCodes.ERROR_CODE == "177"
    assert codes["DO_NOT_DISTURB"] == TuyaCodes.DO_NOT_DISTURB == "157"
    assert codes["BOOST_IQ"] == TuyaCodes.BOOST_IQ == "159"


@pytest.mark.parametrize(
    ("value", "payload"),
    [("auto", "BBoCCAE="), ("pause", "AggN"), ("return", "AggG"), ("Spot", "AA==")],
)
def test_mode_command_values(value, payload):
    assert t2267_model().getRoboVacCommandValue(RobovacCommand.MODE, value) == payload


def test_unknown_command_value_passes_through():
    assert t2267_model().getRoboVacCommandValue(RobovacCommand.MODE, "edge") == "edge"
