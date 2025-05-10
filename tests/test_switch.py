import pytest

async def test_switch_platform(hass, config_entry):
    """Er moet minstens één switch worden aangemaakt."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    switches = hass.states.async_entity_ids("switch")
    assert len(switches) >= 1
