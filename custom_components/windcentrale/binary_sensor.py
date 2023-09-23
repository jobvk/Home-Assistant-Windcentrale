"""Platform for binary_sensor integration."""
import logging
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Add sensors for the passed config_entry in HA."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = [PulsingSensor(windturbine) for windturbine in wind.windturbines]

    if new_entities:
        async_add_entities(new_entities)

class SensorBase(RestoreEntity, BinarySensorEntity):
    """Base representation of a windcentrale turbine."""

    def __init__(self, windturbine) -> None:
        """Initialize the sensor."""
        self._windturbine = windturbine

    @property
    def device_info(self) -> dict[str, str]:
        """Information about this wind turbine"""
        return {
            "identifiers": {(DOMAIN, self._windturbine.id)},
            "name": self._windturbine.name,
            "model": self._windturbine.model,
            "manufacturer": self._windturbine.manufacturer,
        }

    @property
    def available(self) -> bool:
        """Return true if windturbine live sensor is available."""
        return True

class PulsingSensor(SensorBase):
    """Representation of a Sensor."""

    def __init__(self, windturbine):
        """Initialize the sensor."""
        super().__init__(windturbine)

    @property
    def unique_id(self) -> str:
        """Unique ID for the sensor."""
        return f"{self._windturbine.name} Pulsating"

    @property
    def name(self) -> str:
        """Name for the sensor."""
        return f"{self._windturbine.name} Pulsating"

    @property
    def state(self) -> bool:
        """State value for the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Icon for the sensor."""
        return "mdi:pulse"

    async def async_added_to_hass(self) -> None:
        """Call when the entity is about to be added to Home Assistant."""
        if (state := await self.async_get_last_state()) is None:
            self._state = None
            return

        self._state = state.state

    def update(self) -> None:
        """Update the sensor."""
        try:
            self._state = self._windturbine.live_data["pulsating"]
        except Exception as exc:
            _LOGGER.error('There was a exception when updating live binary_sensor with type pulsating.\n\nThe data of the sensor: {}\n\nThe total live data: {}\n\nThe type of the data: {}\n\nWith the exception: {}'.format(self._windturbine.live_data["pulsating"], self._windturbine.live_data, type(self._windturbine.live_data), exc))