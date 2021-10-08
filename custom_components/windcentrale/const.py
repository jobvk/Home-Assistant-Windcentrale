"""Constants for the Windcentrale integration."""
import datetime

from homeassistant.const import (
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_TIMESTAMP,
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

CONF_WINDTURBINE_DE_GROTE_GEERT = "de_grote_geert"
CONF_WINDTURBINE_DE_JONGE_HELD = "de_jonge_held"
CONF_WINDTURBINE_HET_RODE_HERT = "het_rode_hert"
CONF_WINDTURBINE_DE_RANKE_ZWAAN = "de_ranke_zwaan"
CONF_WINDTURBINE_DE_WITTE_JUFFER = "de_witte_juffer"
CONF_WINDTURBINE_DE_BONTE_HEN = "de_bonte_hen"
CONF_WINDTURBINE_DE_TROUWE_WACHTER = "de_trouwe_wachter"
CONF_WINDTURBINE_DE_BLAUWE_REIGER = "de_blauwe_reiger"
CONF_WINDTURBINE_DE_VIER_WINDEN = "de_vier_winden"
CONF_WINDTURBINE_DE_BOERENZWALUW = "de_boerenzwaluw"
CONF_WINDTURBINE_HET_VLIEGEND_HERT = "het_vliegend_hert"

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
# Id: [Config, Name, number, Manufacturer, Model, Latitude, Longitude, StartDate]
WINDTURBINES_LIST = {
    'de_grote_geert': [CONF_WINDTURBINE_DE_GROTE_GEERT, 'De Grote Geert', 1, 'Enercon', 'E-70', "Meedhuizen", 53.27988, 6.9594, datetime.datetime(2013, 1, 1)],
    'de_jonge_held': [CONF_WINDTURBINE_DE_JONGE_HELD, 'De Jonge Held', 2, 'Enercon', 'E-70', "Meedhuizen", 53.27725, 6.95859, datetime.datetime(2013, 1, 1)],
    'het_rode_hert': [CONF_WINDTURBINE_HET_RODE_HERT, 'Het Rode Hert', 31, 'Vestas', 'V80', "Culemborg", 51.935829, 5.192112, datetime.datetime(2014, 1, 1)] ,
    'de_ranke_zwaan': [CONF_WINDTURBINE_DE_RANKE_ZWAAN, 'De Ranke Zwaan', 41, 'Vestas', 'V80', "Culemborg", 51.934916, 5.199874, datetime.datetime(2014, 1, 1)],
    'de_witte_juffer': [CONF_WINDTURBINE_DE_WITTE_JUFFER, 'De Witte Juffer', 51, 'Vestas', 'V80', "Culemborg", 51.935174, 5.195846, datetime.datetime(2014, 1, 1)],
    'de_bonte_hen': [CONF_WINDTURBINE_DE_BONTE_HEN, 'De Bonte Hent', 111, 'Vestas', 'V52', "Burgerbrug", 52.757049, 4.684686, datetime.datetime(2014, 1, 1)],
    'de_trouwe_wachter': [CONF_WINDTURBINE_DE_TROUWE_WACHTER, 'De Trouwe Wachter', 121, 'Vestas', 'V52', "Burgerbrug", 52.758741, 4.686049, datetime.datetime(2014, 1, 1)],
    'de_blauwe_reiger': [CONF_WINDTURBINE_DE_BLAUWE_REIGER, 'De Blauwe Reiger', 131, 'Vestas', 'V52', "Burgerbrug", 52.760478, 4.687449, datetime.datetime(2014, 1, 1)],
    'de_vier_winden': [CONF_WINDTURBINE_DE_VIER_WINDEN, 'De Vier Winden', 141, 'Vestas', 'V52', "Burgerbrug", 52.762214, 4.688828, datetime.datetime(2014, 7, 1)],
    'de_boerenzwaluw': [CONF_WINDTURBINE_DE_BOERENZWALUW, 'De Boerenzwaluw', 191, 'Enercon', 'E-44', "Burum", 53.265376, 6.214152, datetime.datetime(2016, 8, 1)],
    'het_vliegend_hert': [CONF_WINDTURBINE_HET_VLIEGEND_HERT, 'Het Vliegend Hert', 211, 'Lagerwey', 'L82', "Rouveen", 52.59131, 6.22014, datetime.datetime(2018, 9, 15)]
}

# Format:
# Id: [Name, Device Class, Unit Of Measurement, Icon, Json Key]
LIVE_SENSOR_TYPES = {
    'windturbine': [None, DEVICE_CLASS_POWER, POWER_WATT, 'mdi:wind-turbine', 'powerAbsWd'],
    'windspeed': ['Wind Speed', None, 'BFT', 'mdi:windsock', 'windSpeed'],
    'winddirection': ['Wind Direction', None, None, 'mdi:compass', 'windDirection'],
    'powerabstot': ['Power Production Total', DEVICE_CLASS_POWER, POWER_KILO_WATT, None, 'powerAbsTot'],
    'powerabswd': ['Power Production Per Share', DEVICE_CLASS_POWER, POWER_WATT, None, 'powerAbsWd'],
    'powerrel': ['Max Power', None, PERCENTAGE, 'mdi:chart-timeline-variant', 'powerRel'],
    'rpm': ['Revolutions Per Minute', None, 'RPM', 'mdi:speedometer', 'rpm'],
    'kwh': ['kWh', DEVICE_CLASS_ENERGY, ENERGY_KILO_WATT_HOUR, None, 'kwh'],
    'hoursrunthisyear': ['Hours Run This Year', None, TIME_HOURS, 'mdi:calendar-clock', 'hoursRunThisYear'],
    'runpercentage': ['Run Percentage', None, PERCENTAGE, 'mdi:percent', 'runPercentage'],
    'timestamp': ['Last Update', DEVICE_CLASS_TIMESTAMP, None, None, 'timestamp']
}

# Format:
# Id: [Name, Unit Of Measurement, Device Class, XML Key]
PRODUCTION_SENSOR_TYPES = {
    'day': ['Day Production', ENERGY_WATT_HOUR, DEVICE_CLASS_ENERGY, 'DAY'],
    'week': ['Week Production', ENERGY_KILO_WATT_HOUR, DEVICE_CLASS_ENERGY, 'WEEK'],
    'month': ['Month Production', ENERGY_KILO_WATT_HOUR, DEVICE_CLASS_ENERGY, 'MONTH'],
    'year': ['Year Production', 'MWh', DEVICE_CLASS_ENERGY, 'YEAR'],
    'lifetime': ['Total Production', 'MWh', DEVICE_CLASS_ENERGY, 'LIFETIME']
}