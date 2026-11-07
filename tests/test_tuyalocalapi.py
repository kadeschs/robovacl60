"""Tests for TuyaDevice state handling (no network)."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

from custom_components.robovacl60.tuyalocalapi import TuyaDevice
from custom_components.robovacl60.vacuums.T2267 import T2267


def fake_device(dps: dict, reply_dps: dict | None):
    """A stand-in carrying just what TuyaDevice.async_get touches."""
    device = SimpleNamespace(
        gateway_id="gw",
        device_id="dev",
        version=(3, 3),
        model_details=T2267,
        _dps=dict(dps),
        _listeners={},
        _async_send=AsyncMock(),
    )
    reply = None if reply_dps is None else SimpleNamespace(payload={"dps": reply_dps})
    device.async_receive = AsyncMock(return_value=reply)
    device.async_update_state = AsyncMock(
        side_effect=lambda message: device._dps.update(message.payload["dps"])
    )
    return device


async def test_get_clears_stale_connection_failed():
    """Regression: 177 is never in L60 GET replies, so the sentinel used to stick."""
    device = fake_device({"177": "CONNECTION_FAILED"}, {"163": 100})
    await TuyaDevice.async_get(device)
    assert "177" not in device._dps
    assert device._dps["163"] == 100


async def test_get_keeps_real_error_payload():
    device = fake_device({"177": "DAich8KqlJbzzgFSAA=="}, {"163": 100})
    await TuyaDevice.async_get(device)
    assert device._dps["177"] == "DAich8KqlJbzzgFSAA=="


async def test_failed_get_leaves_sentinel():
    device = fake_device({"177": "CONNECTION_FAILED"}, None)
    await TuyaDevice.async_get(device)
    assert device._dps["177"] == "CONNECTION_FAILED"


async def test_update_state_merges_dps():
    device = SimpleNamespace(_dps={"153": "AhAB"}, _LOGGER=SimpleNamespace(debug=lambda *a: None))
    message = SimpleNamespace(payload={"dps": {"163": 99}})
    await TuyaDevice.async_update_state(device, message)
    assert device._dps == {"153": "AhAB", "163": 99}
