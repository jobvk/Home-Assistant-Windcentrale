"""Constants for the Windcentrale integration."""
import json
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

CONF_TOKEN_HEADER = "token_header"
CONF_NEWS_FILTER = "news_filter"

LIVE_INTERVAL = 10 #sec
PRODUCTION_INTERVAL = 1 #min
NEWS_INTERVAL = 5 #min
TOKEN_INTERVAL = 55 #min

DEFAULT_NEWS_FILTER = NEWS_FILTER[0]
DEFAULT_SHOW_ON_MAP = False

# Format:
# Name: [Manufacturer, Model, Location, Latitude, Longitude, Total Shares, StartDate]
WINDTURBINES_LIST = {
    "De Grote Geert": ["Enercon", "E-70", "Meedhuizen", 53.27988, 6.9594, 9910, dt.datetime(2013, 1, 1)],
    "De Jonge Held": ["Enercon", "E-70", "Meedhuizen", 53.27725, 6.95859, 10154, dt.datetime(2013, 1, 1)],
    "Het Rode Hert": ["Vestas", "V80", "Culemborg", 51.935829, 5.192112, 6648, dt.datetime(2014, 1, 1)] ,
    "De Ranke Zwaan": ["Vestas", "V80", "Culemborg", 51.934916, 5.199874, 6164, dt.datetime(2014, 1, 1)],
    "De Witte Juffer": ["Vestas", "V80", "Culemborg", 51.935174, 5.195846, 5721, dt.datetime(2014, 1, 1)],
    "De Bonte Hen": ["Vestas", "V52", "Burgerbrug", 52.757049, 4.684686, 5579, dt.datetime(2014, 1, 1)],
    "De Trouwe Wachter": ["Vestas", "V52", "Burgerbrug", 52.758741, 4.686049, 5602, dt.datetime(2014, 1, 1)],
    "De Blauwe Reiger": ["Vestas", "V52", "Burgerbrug", 52.760478, 4.687449, 5534, dt.datetime(2014, 1, 1)],
    "De Vier Winden": ["Vestas", "V52", "Burgerbrug", 52.762214, 4.688828, 5512, dt.datetime(2014, 7, 1)],
    "De Boerenzwaluw": ["Enercon", "E-44", "Burum", 53.265376, 6.214152, 3000, dt.datetime(2016, 8, 1)],
    "Het Vliegend Hert": ["Lagerwey", "L82", "Rouveen", 52.59131, 6.22014, 9751, dt.datetime(2018, 9, 15)]
}

# Format:
# Id: [Name, Device Class, Unit Of Measurement, Icon, Json Key]
LIVE_SENSOR_TYPES = {
    "windturbine": [None, SensorDeviceClass.POWER, POWER_WATT, "mdi:wind-turbine", "power_per_share"],
    "windspeed": ["Wind Speed", None, "BFT", "mdi:windsock", "wind_power"],
    "winddirection": ["Wind Direction", None, None, "mdi:compass", "wind_direction"],
    "powertotal": ["Power Total", SensorDeviceClass.POWER, POWER_KILO_WATT, None, "power"],
    "powerpershare": ["Power Per Share", SensorDeviceClass.POWER, POWER_WATT, None, "power_per_share"],
    "powerpercentage": ["Power Percentage", None, PERCENTAGE, "mdi:percent", "power_percentage"],
    "rpm": ["Revolutions Per Minute", None, "RPM", "mdi:speedometer", "rpm"],
    "energy": ["Energy Management", SensorDeviceClass.ENERGY, ENERGY_KILO_WATT_HOUR, None, "year_production"],
    "yearproduction": ["Production This Year", SensorDeviceClass.ENERGY, ENERGY_KILO_WATT_HOUR, None, "year_production"],
    "runtimeyear": ["Hours Run This Year", None, TIME_HOURS, "mdi:calendar-clock", "year_runtime"],
    "runtimetotal": ["Hours Run Total", None, TIME_HOURS, "mdi:calendar-clock", "total_runtime"],
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
    def __init__(self, windturbine_name, windturbine_code, windturbine_shares): 
        self.name = windturbine_name
        self.code = windturbine_code
        self.shares = windturbine_shares
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)