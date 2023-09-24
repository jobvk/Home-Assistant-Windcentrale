"""The Windcentrale integration."""
import asyncio
from homeassistant import config_entries, core
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS
from . import wind

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Windcentrale component."""
    # Ensure our namespace for storing objects is a known type.
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Set up Windcentrale from a config entry."""

    # Store an instance of the class.
    hass.data[DOMAIN][entry.entry_id] = wind.Wind(hass, entry)

    # This creates an HA object for each platform.
    for component in PLATFORMS:
        hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, component))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, component) for component in PLATFORMS]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok