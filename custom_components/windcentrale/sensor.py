"""Platform for sensor integration."""
import logging
import dateutil.relativedelta
from datetime import timedelta, datetime
from .const import DOMAIN, PRODUCTION_SENSOR_TYPES
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    wind = hass.data[DOMAIN][config_entry.entry_id]

    await wind.update_token_now()
    await wind.schedule_update_token(timedelta())

    new_entities = []
    for windturbine in wind.windturbines:
        for production_sensor in PRODUCTION_SENSOR_TYPES:
            new_entities.append(ProductionSensor(windturbine, production_sensor.lower()))
        await windturbine.schedule_update_production(timedelta())

    new_entities.append(NewsSensor(wind))
    await wind.schedule_update_news(timedelta())

    if new_entities:
        async_add_entities(new_entities)

class SensorBase(RestoreEntity, SensorEntity):
    """Base representation of a windcentrale turbine."""

    def __init__(self, windturbine):
        """Initialize the sensor."""
        self._windturbine = windturbine

    @property
    def device_info(self):
        """Information about this wind turbine"""
        return {
            "identifiers": {(DOMAIN, self._windturbine.id)},
            "name": self._windturbine.name,
            "model": self._windturbine.model,
            "manufacturer": self._windturbine.manufacturer,
        }

    @property
    def available(self) -> bool:
        """Return True if windturbine and wind is available."""
        return True

class ProductionSensor(SensorBase):
    """Representation of a Sensor."""
    def __init__(self, windturbine, production_sensor_type):
        """Initialize the sensor."""
        super().__init__(windturbine)
        self.type = production_sensor_type
        self._name = PRODUCTION_SENSOR_TYPES[self.type][0]
        self._unit = PRODUCTION_SENSOR_TYPES[self.type][1]
        self._device_class = PRODUCTION_SENSOR_TYPES[self.type][2]
        self._timeframe_type = PRODUCTION_SENSOR_TYPES[self.type][3]
        self._state = None
        self.attr = {}

    @property
    def unique_id(self) -> str:
        """Unique ID for the sensor."""
        return f"{self._windturbine.name} {self._name}"

    @property
    def name(self) -> str:
        """Name for the sensor."""
        return f"{self._windturbine.name} {self._name}"

    @property
    def device_class(self) -> SensorDeviceClass:
        """Device class of the sensor."""
        return self._device_class

    @property
    def state(self):
        """State value for the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Unit of measurement for the sensor."""
        return self._unit

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the entity."""
        return self.attr

    async def async_added_to_hass(self):
        """Call when entity is about to be added to Home Assistant."""
        if (state := await self.async_get_last_state()) is None:
            self._state = None
            return

        self._state = state.state

        if "Year " + str(datetime.now().year - 1) in state.attributes:
            for i in range(2):
                year = "Year " + str(datetime.now().year - i - 1)
                self.attr[year] = state.attributes[year]
        elif (datetime.now() - dateutil.relativedelta.relativedelta(months=+1)).strftime("%B") in state.attributes:
            for i in range(datetime.now().month - 1):
                month = (datetime.now() - dateutil.relativedelta.relativedelta(months= i+1)).strftime("%B")
                self.attr[month] = state.attributes[month]
        elif "Week " + str(datetime.now().isocalendar().week - 1) in state.attributes:
            for i in range(3):
                week = "Week " + str(datetime.now().isocalendar().week - i - 1)
                self.attr[week] = state.attributes[week]

    def update(self):
        """Update the sensor."""
        try:
            if self.type == "yeartotal" :
                self._state = self._windturbine.production_windtrubine_year_api.response_data[datetime.now().year]
                for i in range(2):
                    self.attr["Year " + str(datetime.now().year - i - 1)] = self._windturbine.production_windtrubine_year_api.response_data[datetime.now().year - i - 1]
        except KeyError as keyecx:
            _LOGGER.warning('The year {} is missing in total production data'.format(keyecx))
        except Exception as exc:
            _LOGGER.error('There was an exception when updating total year production data. The error: {}'.format(exc))

        try:
            if self.type == "monthtotal":
                self._state = self._windturbine.production_windtrubine_month_api.response_data[datetime.now().month]
                for i in range(datetime.now().month - 1):
                    month = datetime.now() - dateutil.relativedelta.relativedelta(months= i+1)
                    self.attr[month.strftime("%B")] = self._windturbine.production_windtrubine_month_api.response_data[datetime.now().month - i - 1]
        except KeyError as keyecx:
            _LOGGER.warning('The month {} is missing in total production data'.format(keyecx))
        except Exception as exc:
            _LOGGER.error('There was an exception when updating total month production data. The error: {}'.format(exc))

        try:
            if self.type == "weektotal":
                self._state = self._windturbine.production_windtrubine_week_api.response_data[datetime.now().isocalendar().week]
                for i in range(3):
                    self.attr["Week " + str(datetime.now().isocalendar().week - i - 1)] = self._windturbine.production_windtrubine_week_api.response_data[datetime.now().isocalendar().week - i - 1]
        except KeyError as keyecx:
            _LOGGER.warning('The week {} is missing in total production data'.format(keyecx))
        except Exception as exc:
            _LOGGER.error('There was an exception when updating total week production data. The error: {}'.format(exc))

        try:
            if self.type == "yearshares" :
                self._state = self._windturbine.production_shares_year_api.response_data[datetime.now().year]
                for i in range(2):
                    self.attr["Year " + str(datetime.now().year - i - 1)] = self._windturbine.production_shares_year_api.response_data[datetime.now().year - i - 1]
        except KeyError as keyecx:
            _LOGGER.warning('The year {} is missing in shares production data'.format(keyecx))
        except Exception as exc:
            _LOGGER.error('There was an exception when updating shares year production data. The error: {}'.format(exc))

        try:
            if self.type == "monthshares":
                self._state = self._windturbine.production_shares_month_api.response_data[datetime.now().month]
                for i in range(datetime.now().month - 1):
                    month = datetime.now() - dateutil.relativedelta.relativedelta(months= i+1)
                    self.attr[month.strftime("%B")] = self._windturbine.production_shares_month_api.response_data[datetime.now().month - i - 1]
        except KeyError as keyecx:
            _LOGGER.warning('The month {} is missing in shares production data'.format(keyecx))
        except Exception as exc:
            _LOGGER.error('There was an exception when updating shares month production data. The error: {}'.format(exc))

        try:
            if self.type == "weekshares":
                self._state = self._windturbine.production_shares_week_api.response_data[datetime.now().isocalendar().week]
                for i in range(3):
                    self.attr["Week " + str(datetime.now().isocalendar().week - i - 1)] = self._windturbine.production_shares_week_api.response_data[datetime.now().isocalendar().week - i - 1]
        except KeyError as keyecx:
            _LOGGER.warning('The week {} is missing in shares production data'.format(keyecx))
        except Exception as exc:
            _LOGGER.error('There was an exception when updating shares week production data. The error: {}'.format(exc))

class NewsSensor(RestoreEntity, SensorEntity):
    def __init__(self, wind):
        """Initialize the sensor."""
        self.wind = wind
        self.news_item = self.wind.newsapi.response_data
        self._state = "News"

    @property
    def unique_id(self) -> str:
        """Unique ID for the sensor."""
        return "the windcentrale news"

    @property
    def name(self) -> str:
        """Name for the sensor."""
        return "The Windcentrale News"

    @property
    def state(self) -> str:
        """Static news value for the news sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Icon for the sensor."""
        return "mdi:information"

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the entity."""
        attr = {}
        attr["News Item"] = self.news_item
        return attr

    async def async_added_to_hass(self):
        """Call when entity is about to be added to Home Assistant."""
        if (state := await self.async_get_last_state()) is None:
            self._state = "News"
            return

        self._state = state.state

        if "News Item" in state.attributes:
            self.news_item = state.attributes["News Item"]

    def update(self):
        """Update the sensor."""
        self.news_item = self.wind.newsapi.response_data