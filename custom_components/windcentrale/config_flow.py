"""Config flow for windcentrale integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_SHOW_ON_MAP 
from homeassistant.core import callback
from .const import *
from .wind import Credentials


_LOGGER = logging.getLogger(__name__)

WINDTURBINE_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Windcentrale."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            try:
                windcentrale_data = await validate_input(self.hass, user_input)
                return self.async_create_entry(title="Windcentrale", data=windcentrale_data)
            except BadCredentials:
                errors["base"] = "bad_credentials"
            except Exception:
                _LOGGER.error("Unexpected exception when submitting windcentrale config")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(step_id="user", data_schema=WINDTURBINE_SCHEMA, errors=errors)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize The Windcentrale options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the Windcentrale options."""
        errors = {}
        if user_input is not None:
            try:
                return self.async_create_entry(title="", data=user_input)
            except Exception:
                _LOGGER.error("Unexpected exception when chaning windcentrale options")
                errors["base"] = "unknown"

        return self.async_show_form(step_id="init", data_schema= vol.Schema({   
            vol.Optional(CONF_OPTIONS_LIVE, default=self.config_entry.options.get(CONF_OPTIONS_LIVE, DEFAULT_LIVE)): bool,
            vol.Optional(CONF_OPTIONS_LIVE_INTERVAL, default=self.config_entry.options.get(CONF_OPTIONS_LIVE_INTERVAL, DEFAULT_LIVE_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=20, max=300)),
            vol.Optional(CONF_OPTIONS_PRODUCTION, default=self.config_entry.options.get(CONF_OPTIONS_PRODUCTION, DEFAULT_PRODUCTION)): bool,
            vol.Optional(CONF_OPTIONS_PRODUCTION_INTERVAL, default=self.config_entry.options.get(CONF_OPTIONS_PRODUCTION_INTERVAL, DEFAULT_PRODUCTION_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            vol.Optional(CONF_OPTIONS_NEWS, default=self.config_entry.options.get(CONF_OPTIONS_NEWS, DEFAULT_NEWS)): bool,
            vol.Optional(CONF_OPTIONS_NEWS_FILTER, default=self.config_entry.options.get(CONF_OPTIONS_NEWS_FILTER, NEWS_FILTER[0])): vol.In(NEWS_FILTER),
            vol.Optional(CONF_OPTIONS_NEWS_INTERVAL, default=self.config_entry.options.get(CONF_OPTIONS_NEWS_INTERVAL, DEFAULT_NEWS_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            vol.Optional(CONF_SHOW_ON_MAP, default=self.config_entry.options.get(CONF_SHOW_ON_MAP, DEFAULT_SHOW_ON_MAP)): bool,
        }), 
        errors=errors)

async def validate_input(hass, data: dict):
    """Validate the user input"""
    windCredentials = Credentials(hass, data[CONF_EMAIL], data[CONF_PASSWORD])
    result = await windCredentials.test_credentails()
    if result == "Bad credentials":
        raise BadCredentials
    elif result == 'error':
        raise Exception
    elif result == 'succes':
        windshare_dict = await windCredentials.collect_windshares()
        for windturbine in WINDTURBINES_LIST:
            if windturbine in windshare_dict:
                data[windturbine] = windshare_dict[windturbine]["shares"]
            else:
                data[windturbine] = 0
    return data

class BadCredentials(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid number."""