"""Test fixtures for the Eufy RoboVac L60 (T2267) integration."""

import os
import sys
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_DESCRIPTION,
    CONF_ID,
    CONF_IP_ADDRESS,
    CONF_MAC,
    CONF_MODEL,
    CONF_NAME,
)

# Make custom_components importable from the repository root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from custom_components.robovacl60.robovac import RoboVac  # noqa: E402
from custom_components.robovacl60.vacuums.T2267 import T2267  # noqa: E402


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for testing."""
    yield


def t2267_model() -> RoboVac:
    """Return a RoboVac carrying the real T2267 model details, without networking.

    RoboVac.__init__ would start TuyaDevice's queue task; the model-detail helpers
    only need ``model_details``.
    """
    vac = RoboVac.__new__(RoboVac)
    vac.model_details = T2267
    vac.model_code = "T2267"
    return vac


@pytest.fixture
def mock_robovac():
    """A mocked T2267 device whose model helpers are the real implementation."""
    model = t2267_model()
    mock = MagicMock()
    mock.getHomeAssistantFeatures.return_value = model.getHomeAssistantFeatures()
    mock.getRoboVacFeatures.return_value = model.getRoboVacFeatures()
    mock.getFanSpeeds.return_value = model.getFanSpeeds()
    mock.getDpsCodes.return_value = model.getDpsCodes()
    mock.getRoboVacCommandValue.side_effect = model.getRoboVacCommandValue
    mock._dps = {}
    mock.async_get = AsyncMock(return_value=None)
    mock.async_set = AsyncMock(return_value=None)
    mock.async_disconnect = AsyncMock(return_value=None)
    mock.async_disable = AsyncMock(return_value=None)
    return mock


@pytest.fixture
def mock_vacuum_data():
    """Config data for one L60 vacuum, as stored in the config entry."""
    return {
        CONF_NAME: "Basement",
        CONF_ID: "test_l60_id",
        CONF_MODEL: "T2267",
        CONF_IP_ADDRESS: "192.168.1.45",
        CONF_ACCESS_TOKEN: "0123456789abcdef",
        CONF_DESCRIPTION: "eufy Clean L60",
        CONF_MAC: "aa:bb:cc:dd:ee:11",
    }
