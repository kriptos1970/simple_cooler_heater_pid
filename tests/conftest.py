import pytest

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.simple_pid_controller.const import DOMAIN, CONF_SENSOR_ENTITY_ID

@pytest.fixture
def config_entry(hass):
    """Maak een MockConfigEntry en voeg ’m toe aan hass."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Test PID Controller",
        data={CONF_SENSOR_ENTITY_ID: "sensor.test"},
        options={},
    )
    entry.add_to_hass(hass)
    return entry
