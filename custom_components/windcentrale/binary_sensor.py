"""Platform for binary_sensor integration."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for windturbine in wind.windturbines:
        if wind.live == True:
            new_devices.append(PulsingSensor(windturbine))

    if new_devices:
        async_add_devices(new_devices)

class SensorBase(BinarySensorEntity):
    """Base representation of a windcentrale turbine."""

    def __init__(self, windturbine):
        """Initialize the sensor."""
        self._windturbine = windturbine

    @property
    def device_info(self):
        """Information about this wind turbine"""
        return {
            "identifiers": {(DOMAIN, self._windturbine.windturbine_id)},
            "name": self._windturbine.name,
            "model": self._windturbine.model,
            "manufacturer": self._windturbine.manufacturer,
        }

    @property
    def available(self):
        """Return true if windturbine live sensor is available."""
        return self._windturbine.live_status

class PulsingSensor(SensorBase):
    """Representation of a Sensor."""

    def __init__(self, windturbine):
        """Initialize the sensor."""
        super().__init__(windturbine)
        self._state = None

    @property
    def unique_id(self):
        """Unique ID for the sensor."""
        return f"{self._windturbine.name} Pulsating"

    @property
    def name(self):
        """Name for the sensor."""
        return f"{self._windturbine.name} Pulsating"

    @property
    def state(self):
        """State value for the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon for the sensor."""
        return "mdi:pulse"

    def update(self):
        """Update the sensor."""
        if self._windturbine.live_data:
            self._state = self._windturbine.live_data["pulsating"]
            return self._state
        else:
            return None