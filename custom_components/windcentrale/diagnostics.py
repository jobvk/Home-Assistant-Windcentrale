"""Diagnostics for the Windcentrale integration."""
from __future__ import annotations
from typing import Any
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import *

TO_REDACT = {
    CONF_EMAIL,
    CONF_PASSWORD,
}

async def async_get_config_entry_diagnostics(hass, config_entry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    windturbine_data = []
    for windturbine in wind.windturbines:
        windturbine_data.append({
            "name": windturbine.name,
            "id": windturbine.id,
            "shares": windturbine.shares,
            "manufacturer": windturbine.manufacturer,
            "model": windturbine.model,
            "location": windturbine.location,
            "latitude": windturbine.latitude,
            "longitude": windturbine.longitude,
            "total_shares": windturbine.total_shares,
            "start_date": windturbine.start_date,
            "energy_prognoses": windturbine.energy_prognoses,
            "data": {
                "live_data": windturbine.live_data,
                "production_windtrubine_year_data": windturbine.production_windtrubine_year_data,
                "production_windtrubine_month_data": windturbine.production_windtrubine_month_data,
                "live_production_windtrubine_week_datadata": windturbine.production_windtrubine_week_data,
                "production_shares_year_data": windturbine.production_shares_year_data,
                "production_shares_month_data": windturbine.production_shares_month_data,
                "production_shares_week_data": windturbine.production_shares_week_data
            }
        })

    return {
        "entry_data": async_redact_data(config_entry.data, TO_REDACT),
        "entry_options": async_redact_data(config_entry.options, TO_REDACT),
        "const": {
            "domain": DOMAIN,
            "default_show_on_map": DEFAULT_SHOW_ON_MAP,
            "conf_windtubines": CONF_WINDTURBINES,
            "intervals": {
                "live": LIVE_INTERVAL,
                "production": PRODUCTION_INTERVAL,
                "news": NEWS_INTERVAL,
                "token": TOKEN_INTERVAL
            },
            "platforms": PLATFORMS,
            "platform_select": PLATFORM_SELECT,
            "platform": {
                "windcentrale": {
                    "base_url": WINDCENTRALE_BASE_URL,
                    "pool_id": WINDCENTRALE_POOL_ID,
                    "client_id": WINDCENTRALE_CLIENT_ID
                },
                "winddelen": {
                    "base_url": WINDDELEN_BASE_URL,
                    "pool_id": WINDDELEN_POOL_ID,
                    "client_id": WINDDELEN_CLIENT_ID
                }
            }
        },
        "wind": {
            "domain": wind.id,
            "show_on_map": wind.show_on_map,
            "base_url": wind.base_url,
        },
        "sensors": {
            "news_data": wind.news_data,
            "windturbines": windturbine_data
        }
    }