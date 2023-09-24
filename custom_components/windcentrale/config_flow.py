"""Config flow for windcentrale integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_PLATFORM, CONF_SHOW_ON_MAP
from homeassistant.core import callback
from .const import *
from .wind import Credentials

_LOGGER = logging.getLogger(__name__)

WINDTURBINE_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required(CONF_PLATFORM, default=PLATFORM_SELECT[0]): vol.In(PLATFORM_SELECT),
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Windcentrale."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None) -> dict:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            try:
                user_input = await validate_input(self.hass, user_input)
                return self.async_create_entry(title="Windcentrale", data=user_input)
            except InvalidSignInUserParameters:
                errors["base"] = "invalid_parameter"
            except InvalidSignInUserCredentials:
                errors["base"] = "invalid_user_credentials"
            except InvalidSignInTooManyRequests:
                errors["base"] = "invalid_too_many_requests"
            except InvalidSignInTooUnknownError:
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(step_id="user", data_schema=WINDTURBINE_SCHEMA, errors=errors)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry) -> None:
        """Initialize The Windcentrale options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> dict:
        """Manage the Windcentrale options."""
        errors = {}
        if user_input is not None:
            try:
                return self.async_create_entry(title="", data=user_input)
            except Exception as exc:
                _LOGGER.error(f"Unexpected exception when changing windcentrale options: {exc}")
                errors["base"] = "unknown"

        return self.async_show_form(step_id="init", data_schema=vol.Schema({
            vol.Optional(CONF_SHOW_ON_MAP, default=self.config_entry.options.get(CONF_SHOW_ON_MAP, DEFAULT_SHOW_ON_MAP)): bool
        }),
        errors=errors)

async def validate_input(hass, user_input: dict) -> dict:
    """Validate the user input."""
    credentials = Credentials(hass, user_input[CONF_EMAIL], user_input[CONF_PASSWORD], user_input[CONF_PLATFORM])
    result_user_credentials = await credentials.authenticate_user_credentials()
    
    if result_user_credentials == "invalid_parameter":
        raise InvalidSignInUserParameters
    elif result_user_credentials == "invalid_user_credentials":
        raise InvalidSignInUserCredentials
    elif result_user_credentials == "invalid_too_many_requests":
        raise InvalidSignInTooManyRequests
    elif result_user_credentials == "unknown":
        raise InvalidSignInTooUnknownError
    else:
        user_input[CONF_WINDTURBINES] = []
        result_projects_windshares = await credentials.collect_projects_windshares()
        for windturbine in result_projects_windshares.keys():
            user_input[CONF_WINDTURBINES].append(result_projects_windshares[windturbine].to_dict())
    return user_input

class InvalidSignInUserParameters(exceptions.HomeAssistantError):
    """Error to indicate there's a missing username or password."""

class InvalidSignInUserCredentials(exceptions.HomeAssistantError):
    """Error to indicate incorrect username or password."""

class InvalidSignInTooManyRequests(exceptions.HomeAssistantError):
    """Error to indicate there are too many requests to the server."""

class InvalidSignInTooUnknownError(exceptions.HomeAssistantError):
    """Error to indicate an unknown error occurred."""