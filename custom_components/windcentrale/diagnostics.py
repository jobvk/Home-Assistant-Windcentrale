"""Diagnostics for the Windcentrale integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .const import DOMAIN

TO_REDACT = {
    CONF_EMAIL,
    CONF_PASSWORD,
}

async def async_get_config_entry_diagnostics(hass, config_entry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    return {
        "entry_data": async_redact_data(config_entry.data, TO_REDACT),
        "entry_options": async_redact_data(config_entry.options, TO_REDACT)
    }