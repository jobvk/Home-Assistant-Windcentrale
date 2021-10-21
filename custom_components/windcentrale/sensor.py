"""Platform for sensor integration."""
import math
from homeassistant.components.sensor import SensorEntity
from datetime import timedelta
from .const import DOMAIN, LIVE_SENSOR_TYPES, PRODUCTION_SENSOR_TYPES
from homeassistant.const import ATTR_LOCATION, ATTR_LATITUDE, ATTR_LONGITUDE

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    for windturbine in wind.windturbines:
        if wind.live == True:
            for live_sensors in LIVE_SENSOR_TYPES:
                live_sensor_type = live_sensors.lower()
                new_entities.append(LiveSensor(windturbine, live_sensor_type))

        await windturbine.schedule_update_live(timedelta())

        if wind.production == True:
            for production_sensors in PRODUCTION_SENSOR_TYPES:
                production_sensor_type = production_sensors.lower()
                new_entities.append(ProductionSensor(windturbine, production_sensor_type))

        await windturbine.schedule_update_production(timedelta())

    if wind.news == True:
        new_entities.append(NewsSensor(wind))
        await wind.schedule_update_news(timedelta())

    if new_entities:
        async_add_entities(new_entities)

class SensorBase(SensorEntity):
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

class LiveSensor(SensorBase):
    """Representation of a Sensor."""

    def __init__(self, windturbine, live_sensor_type):
        """Initialize the sensor."""
        super().__init__(windturbine)
        self.type = live_sensor_type
        self._name = LIVE_SENSOR_TYPES[self.type][0]
        self._device_class = LIVE_SENSOR_TYPES[self.type][1]
        self._unit = LIVE_SENSOR_TYPES[self.type][2]
        self._icon = LIVE_SENSOR_TYPES[self.type][3]
        self._sensor = LIVE_SENSOR_TYPES[self.type][4]
        self._state = None
        self.degrees = {
                "N":0,
                "NO":45,
                "O":90,
                "ZO":135,
                "Z":180,
                "ZW":225,
                "W":270,
                "NW":315
            }

    @property
    def unique_id(self):
        """Unique ID for the sensor."""
        if self.type == "windturbine":
            return f"{self._windturbine.name}"
        else:
            return f"{self._windturbine.name} {self._name}"

    @property
    def name(self):
        """Name for the sensor."""
        if self.type == "windturbine":
            return f"{self._windturbine.name}"
        else:
            return f"{self._windturbine.name} {self._name}"

    @property
    def device_class(self):
        """Device class of the sensor."""
        return self._device_class

    @property
    def state(self):
        """State value for the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon for the sensor."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Unit of measurement for the sensor."""
        return self._unit

    @property
    def device_state_attributes(self):
        """Return the state attributes of the entity."""
        attr = {}
        if self.type == "windturbine":
            attr["Id"] = self._windturbine.number
            attr["Shares"] = self._windturbine.shares
            attr[ATTR_LOCATION] = self._windturbine.location
            if self._windturbine.show_on_map:
                attr[ATTR_LATITUDE] = self._windturbine.latitude
                attr[ATTR_LONGITUDE] = self._windturbine.longitude
            else:
                attr["Latitude"]  = self._windturbine.latitude
                attr["Longitude"] = self._windturbine.longitude
            attr["Households"] = math.floor((self._windturbine.live_data["powerAbsTot"] * 1000) / 400)
            attr["Energy-Efficient Bulbs"] = math.floor(self._state / 12)
        elif self.type == "runpercentage":
            attr["Start Date"] = self._windturbine.startDate
        elif self.type == "winddirection":
            attr["Degrees"] = self.degrees.get(self._state)
        elif self.type == "kwh":
            attr["kWh Forecast"] = self._windturbine.live_data["kwhForecast"]
        return attr

    @property
    def available(self):
        """Return True if windturbine and wind is available."""
        return self._windturbine.live_status

    def update(self):
        """Update the sensor."""
        if self._windturbine.live_data:
            if self.type == "windturbine":
                self._state = self._windturbine.live_data[self._sensor] * self._windturbine.shares
            else:
                self._state = self._windturbine.live_data[self._sensor]
            return self._state
        else:
            return None

class ProductionSensor(SensorBase):
    """Representation of a Sensor."""
    def __init__(self, windturbine, production_sensor_type):
        """Initialize the sensor."""
        super().__init__(windturbine)
        self.type = production_sensor_type
        self._name = PRODUCTION_SENSOR_TYPES[self.type][0]
        self._unit = PRODUCTION_SENSOR_TYPES[self.type][1]
        self._device_class = PRODUCTION_SENSOR_TYPES[self.type][2]
        self._sensor = PRODUCTION_SENSOR_TYPES[self.type][3]
        self._state = None
        self._tstart = None
        self._tend = None

    @property
    def unique_id(self):
        """Unique ID for the sensor."""
        return f"{self._windturbine.name} {self._name}"

    @property
    def name(self):
        """Name for the sensor."""
        return f"{self._windturbine.name} {self._name}"

    @property
    def device_class(self):
        """Device class of the sensor."""
        return self._device_class

    @property
    def state(self):
        """State value for the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Unit of measurement for the sensor."""
        return self._unit

    @property
    def device_state_attributes(self):
        """Return the state attributes of the entity."""
        attr = {}
        attr["Start Time"] = self._tstart
        attr["End Time"] = self._tend
        return attr

    @property
    def available(self):
        """Return true if windturbine production sensor is available."""
        return self._windturbine.production_status

    def update(self):
        """Update the sensor."""
        if self._windturbine.production_data:
            self._tstart = self._windturbine.production_data[self._sensor][0]
            self._tend = self._windturbine.production_data[self._sensor][1]
            self._state = self._windturbine.production_data[self._sensor][2]
            return self._tstart and self._tend and self._state
        else:
            return None

class NewsSensor(SensorEntity):
    def __init__(self, wind):
        """Initialize the sensor."""
        self.wind = wind
        self._item = None

    @property
    def unique_id(self):
        """Unique ID for the sensor."""
        return "the windcentrale news"

    @property
    def name(self):
        """Name for the sensor."""
        return "The Windcentrale News"

    @property
    def state(self):
        """Static news value for the news sensor."""
        return "News"

    @property
    def icon(self):
        """Icon for the sensor."""
        return "mdi:information"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the entity."""
        attr = {}
        attr["News Item"] = self._item
        return attr

    @property
    def available(self):
        """Return true if windturbine news sensor is available."""
        return self.wind.news_status

    def update(self):
        """Update the sensor."""
        if self.wind.news_data:
            self._item = self.wind.news_data
            return self._item
        else:
            return None