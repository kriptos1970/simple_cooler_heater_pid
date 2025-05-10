import pytest
from custom_components.simple_pid_controller.number import PID_NUMBER_ENTITIES

async def test_number_platform(hass, config_entry):
    """Controleer dat alle Number-entities uit PID_NUMBER_ENTITIES worden aangemaakt."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    numbers = hass.states.async_entity_ids("number")
    assert len(numbers) == len(PID_NUMBER_ENTITIES)
