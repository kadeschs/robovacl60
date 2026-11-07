"""Tests for the options flow, driven through Home Assistant's flow manager."""

import pytest
from homeassistant import data_entry_flow
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_DESCRIPTION,
    CONF_ID,
    CONF_IP_ADDRESS,
    CONF_MAC,
    CONF_MODEL,
    CONF_NAME,
)
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.robovacl60.const import CONF_AUTODISCOVERY, CONF_VACS, DOMAIN


def _vac(vac_id: str, name: str, ip: str = "") -> dict:
    return {
        CONF_ID: vac_id,
        CONF_NAME: name,
        CONF_MODEL: "T2267",
        CONF_DESCRIPTION: "eufy Clean L60",
        CONF_MAC: "AA:BB:CC:DD:EE:FF",
        CONF_AUTODISCOVERY: True,
        CONF_IP_ADDRESS: ip,
        CONF_ACCESS_TOKEN: "0123456789abcdef",
    }


@pytest.fixture
def config_entry(hass: HomeAssistant) -> MockConfigEntry:
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="test@example.com",
        data={
            CONF_VACS: {
                "vac_1": _vac("vac_1", "Basement"),
                "vac_2": _vac("vac_2", "Upstairs", "192.168.1.50"),
            }
        },
    )
    entry.add_to_hass(hass)
    return entry


async def _select(hass: HomeAssistant, entry: MockConfigEntry, vac_id: str) -> dict:
    result = await hass.config_entries.options.async_init(entry.entry_id)
    return await hass.config_entries.options.async_configure(
        result["flow_id"], {"selected_vacuum": vac_id}
    )


async def test_init_lists_vacuums(hass: HomeAssistant, config_entry):
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "init"
    schema = result["data_schema"].schema
    selector = next(v for k, v in schema.items() if k == "selected_vacuum")
    assert selector.container == {"vac_1": "Basement", "vac_2": "Upstairs"}


async def test_select_shows_edit_form_with_defaults(hass: HomeAssistant, config_entry):
    result = await _select(hass, config_entry, "vac_2")
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "edit"
    defaults = {str(k): k.default() for k in result["data_schema"].schema}
    assert defaults[CONF_AUTODISCOVERY] is True
    assert defaults[CONF_IP_ADDRESS] == "192.168.1.50"


async def test_edit_saves_ip_and_autodiscovery(hass: HomeAssistant, config_entry):
    result = await _select(hass, config_entry, "vac_1")
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_AUTODISCOVERY: False, CONF_IP_ADDRESS: "192.168.1.45"}
    )
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    vac = config_entry.data[CONF_VACS]["vac_1"]
    assert vac[CONF_AUTODISCOVERY] is False
    assert vac[CONF_IP_ADDRESS] == "192.168.1.45"
    # The other vacuum is untouched
    assert config_entry.data[CONF_VACS]["vac_2"][CONF_IP_ADDRESS] == "192.168.1.50"


async def test_edit_blank_ip_keeps_existing(hass: HomeAssistant, config_entry):
    result = await _select(hass, config_entry, "vac_2")
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_AUTODISCOVERY: True, CONF_IP_ADDRESS: ""}
    )
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert config_entry.data[CONF_VACS]["vac_2"][CONF_IP_ADDRESS] == "192.168.1.50"
