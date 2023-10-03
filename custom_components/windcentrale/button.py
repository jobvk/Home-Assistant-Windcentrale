"""Platform for button integration."""
from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add a button for the passed config_entry in HA."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = [ButtonRefreshWindShares(wind)]

    if new_entities:
        async_add_entities(new_entities)

class ButtonRefreshWindShares(ButtonEntity):
    """Representation of a wind share refresh button."""

    def __init__(self, wind) -> None:
        """Initialize the button."""
        self.wind = wind

    @property
    def unique_id(self) -> str:
        """Unique ID for the button."""
        return "the windcentrale update wind shares"

    @property
    def name(self) -> str:
        """Name for the button."""
        return "The Windcentrale Update Wind Shares"

    @property
    def device_class(self) -> ButtonDeviceClass:
        """Device class of the button."""
        return ButtonDeviceClass.UPDATE

    @property
    def entity_category(self) -> EntityCategory:
        """Entity category of the button."""
        return EntityCategory.CONFIG

    @property
    def icon(self) -> str:
        """Icon for the button."""
        return "mdi:cloud-refresh-variant"

    async def async_press(self) -> None:
        """Update the wind shares."""
        await self.wind.update_windturbines()