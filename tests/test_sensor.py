import pytest

async def test_sensor_platform(hass, config_entry):
    """Er moet minstens één sensor worden aangemaakt."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    sensors = hass.states.async_entity_ids("sensor")
    assert len(sensors) >= 1
