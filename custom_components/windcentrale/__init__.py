"""The Windcentrale integration."""
import asyncio
from homeassistant import config_entries, core
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_SHOW_ON_MAP 
from . import wind
from .const import *

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Windcentrale component."""
    # Ensure our name space for storing objects is a known type.
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up Windcentrale from a config entry."""

    # Store an instance of the class.
    hass.data[DOMAIN][entry.entry_id] = wind.Wind(hass, entry)

    # This creates a HA object for each platform.
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok