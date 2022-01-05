"""Constants for the Windcentrale integration."""
import datetime as dt
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    POWER_WATT,
    POWER_KILO_WATT,
    ENERGY_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    TIME_HOURS,
    PERCENTAGE,
)

DOMAIN = "windcentrale"

PLATFORMS = ["sensor","binary_sensor"]
NEWS_FILTER = ["All News", "General + Your Windturbine(s)", "Only Your Windturbine(s)"]

CONF_OPTIONS_LIVE = "live"
CONF_OPTIONS_LIVE_INTERVAL = "live_interval"
CONF_OPTIONS_PRODUCTION = "production"
CONF_OPTIONS_PRODUCTION_INTERVAL = "production_interval"
CONF_OPTIONS_NEWS = "news"
CONF_OPTIONS_NEWS_FILTER = "news_filter"
CONF_OPTIONS_NEWS_INTERVAL = "news_interval"

DEFAULT_LIVE = True
DEFAULT_LIVE_INTERVAL = 60
DEFAULT_PRODUCTION = True
DEFAULT_PRODUCTION_INTERVAL = 5
DEFAULT_NEWS = True
DEFAULT_NEWS_FILTER = NEWS_FILTER[0]
DEFAULT_NEWS_INTERVAL = 15
DEFAULT_SHOW_ON_MAP = False

# Format:
# Name: [id, Manufacturer, Model, Latitude, Longitude, StartDate]
WINDTURBINES_LIST = {
    "De Grote Geert": [1, "Enercon", "E-70", "Meedhuizen", 53.27988, 6.9594, dt.datetime(2013, 1, 1)],
    "De Jonge Held": [2, "Enercon", "E-70", "Meedhuizen", 53.27725, 6.95859, dt.datetime(2013, 1, 1)],
    "Het Rode Hert": [31, "Vestas", "V80", "Culemborg", 51.935829, 5.192112, dt.datetime(2014, 1, 1)] ,
    "De Ranke Zwaan": [ 41, "Vestas", "V80", "Culemborg", 51.934916, 5.199874, dt.datetime(2014, 1, 1)],
    "De Witte Juffer": [51, "Vestas", "V80", "Culemborg", 51.935174, 5.195846,dt.datetime(2014, 1, 1)],
    "De Bonte Hen": [111, "Vestas", "V52", "Burgerbrug", 52.757049, 4.684686, dt.datetime(2014, 1, 1)],
    "De Trouwe Wachter": [121, "Vestas", "V52", "Burgerbrug", 52.758741, 4.686049, dt.datetime(2014, 1, 1)],
    "De Blauwe Reiger": [131, "Vestas", "V52", "Burgerbrug", 52.760478, 4.687449, dt.datetime(2014, 1, 1)],
    "De Vier Winden": [141, "Vestas", "V52", "Burgerbrug", 52.762214, 4.688828, dt.datetime(2014, 7, 1)],
    "De Boerenzwaluw": [191, "Enercon", "E-44", "Burum", 53.265376, 6.214152, dt.datetime(2016, 8, 1)],
    "Het Vliegend Hert": [211, "Lagerwey", "L82", "Rouveen", 52.59131, 6.22014, dt.datetime(2018, 9, 15)]
}

# Format:
# Id: [Name, Device Class, Unit Of Measurement, Icon, Json Key]
LIVE_SENSOR_TYPES = {
    "windturbine": [None, SensorDeviceClass.POWER, POWER_WATT, "mdi:wind-turbine", "powerAbsWd"],
    "windspeed": ["Wind Speed", None, "BFT", "mdi:windsock", "windSpeed"],
    "winddirection": ["Wind Direction", None, None, "mdi:compass", "windDirection"],
    "powerabstot": ["Power Production Total", SensorDeviceClass.POWER, POWER_KILO_WATT, None, "powerAbsTot"],
    "powerabswd": ["Power Production Per Share", SensorDeviceClass.POWER, POWER_WATT, None, "powerAbsWd"],
    "powerrel": ["Max Power", None, PERCENTAGE, "mdi:chart-timeline-variant", "powerRel"],
    "rpm": ["Revolutions Per Minute", None, "RPM", "mdi:speedometer", "rpm"],
    "kwh": ["kWh", SensorDeviceClass.ENERGY, ENERGY_KILO_WATT_HOUR, None, "kwh"],
    "hoursrunthisyear": ["Hours Run This Year", None, TIME_HOURS, "mdi:calendar-clock", "hoursRunThisYear"],
    "runpercentage": ["Run Percentage", None, PERCENTAGE, "mdi:percent", "runPercentage"],
    "timestamp": ["Last Update", SensorDeviceClass.TIMESTAMP, None, None, "timestamp"]
}

# Format:
# Id: [Name, Unit Of Measurement, Device Class, XML Key]
PRODUCTION_SENSOR_TYPES = {
    "day": ["Day Production", ENERGY_WATT_HOUR, SensorDeviceClass.ENERGY, "DAY"],
    "week": ["Week Production", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "WEEK"],
    "month": ["Month Production", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "MONTH"],
    "year": ["Year Production", "MWh", SensorDeviceClass.ENERGY, "YEAR"],
    "lifetime": ["Total Production", "MWh", SensorDeviceClass.ENERGY, "LIFETIME"]
}

class powerProducer: 
    def __init__(self, powerproducer_id, windturbine_id, name): 
        self.id = powerproducer_id 
        self.windturbine_id = windturbine_id
        self.name = name
        self.shares = 0

    def add_shares(self):
        self.shares = self.shares + 1

class Shares: 
    def __init__(self, share_id, powerProducer): 
        self.id = share_id
        self.powerProducer = powerProducer