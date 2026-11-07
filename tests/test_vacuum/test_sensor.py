"""Tests for the L60 battery sensor."""

from types import SimpleNamespace
from unittest.mock import MagicMock

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import PERCENTAGE

from custom_components.robovacl60.const import CONF_VACS, DOMAIN
from custom_components.robovacl60.sensor import RobovacBatterySensor


def make_sensor(mock_vacuum_data, vac_client):
    sensor = RobovacBatterySensor("entry_1", mock_vacuum_data)
    sensor.hass = MagicMock()
    sensor.hass.data = {
        DOMAIN: {"entry_1": {CONF_VACS: {mock_vacuum_data["id"]: vac_client}}}
    }
    return sensor


def test_sensor_init(mock_vacuum_data):
    sensor = RobovacBatterySensor("entry_1", mock_vacuum_data)
    assert sensor.unique_id == "test_l60_id_battery"
    assert sensor.name == "Basement Battery"
    assert sensor.device_class == SensorDeviceClass.BATTERY
    assert sensor.native_unit_of_measurement == PERCENTAGE


async def test_sensor_reads_dps_163(mock_vacuum_data):
    sensor = make_sensor(mock_vacuum_data, SimpleNamespace(tuyastatus={"163": 80}))
    await sensor.async_update()
    assert sensor.native_value == 80
    assert sensor.available is True


async def test_sensor_before_entity_swap(mock_vacuum_data, caplog):
    """Regression: during setup CONF_VACS still holds the raw config dict."""
    sensor = make_sensor(mock_vacuum_data, dict(mock_vacuum_data))
    await sensor.async_update()
    assert sensor.available is False
    assert "Error updating battery sensor" not in caplog.text


async def test_sensor_no_status_yet(mock_vacuum_data):
    sensor = make_sensor(mock_vacuum_data, SimpleNamespace(tuyastatus=None))
    await sensor.async_update()
    assert sensor.available is False


async def test_sensor_missing_vacuum(mock_vacuum_data):
    sensor = make_sensor(mock_vacuum_data, None)
    await sensor.async_update()
    assert sensor.available is False
