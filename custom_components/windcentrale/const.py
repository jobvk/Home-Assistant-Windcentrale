"""Constants for the Windcentrale integration."""
import datetime as dt
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import ENERGY_KILO_WATT_HOUR, Platform

DOMAIN = "windcentrale"

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]

CONF_WINDTURBINES = "windturbines"

PRODUCTION_INTERVAL = 1 #hour
NEWS_INTERVAL = 5 #min
TOKEN_INTERVAL = 55 #min

PLATFORM_SELECT = ["Windcentrale", "Winddelen"]
DEFAULT_SHOW_ON_MAP = False

WINDCENTRALE_BASE_URL = "mijn.windcentrale.nl"
WINDCENTRALE_POOL_ID = "eu-west-1_U7eYBPrBd"
WINDCENTRALE_CLIENT_ID = "715j3r0trk7o8dqg3md57il7q0"

WINDDELEN_BASE_URL = "mijn.winddelen.nl"
WINDDELEN_POOL_ID = "eu-west-1_3ujjjPxxH"
WINDDELEN_CLIENT_ID = "11edho7vncqa74o1bju4tlgnt0"

# Format:
# Name: [Manufacturer, Model, Location, Latitude, Longitude, Total Shares, Start Date, Energy Prognoses (kWh)]
WINDTURBINES_LIST = {
    "De Grote Geert": ["Enercon", "E-70", "Meedhuizen", 53.27988, 6.9594, 9910, dt.datetime(2013, 1, 1), 4900000],
    "De Jonge Held": ["Enercon", "E-70", "Meedhuizen", 53.27725, 6.95859, 10154, dt.datetime(2013, 1, 1), 5000000],
    "Het Rode Hert": ["Vestas", "V80", "Culemborg", 51.935829, 5.192112, 6648, dt.datetime(2014, 1, 1), 3300000] ,
    "De Ranke Zwaan": ["Vestas", "V80", "Culemborg", 51.934916, 5.199874, 6164, dt.datetime(2014, 1, 1), 3000000],
    "De Witte Juffer": ["Vestas", "V80", "Culemborg", 51.935174, 5.195846, 5721, dt.datetime(2014, 1, 1), 2800000],
    "De Bonte Hen": ["Vestas", "V52", "Burgerbrug", 52.757049, 4.684686, 5579, dt.datetime(2014, 1, 1), 2800000],
    "De Trouwe Wachter": ["Vestas", "V52", "Burgerbrug", 52.758741, 4.686049, 5602, dt.datetime(2014, 1, 1), 2800000],
    "De Blauwe Reiger": ["Vestas", "V52", "Burgerbrug", 52.760478, 4.687449, 5534, dt.datetime(2014, 1, 1), 2800000],
    "De Vier Winden": ["Vestas", "V52", "Burgerbrug", 52.762214, 4.688828, 5512, dt.datetime(2014, 7, 1), 2800000],
    "De Boerenzwaluw": ["Enercon", "E-44", "Burum", 53.265376, 6.214152, 3000, dt.datetime(2016, 8, 1), 1500000],
    "Het Vliegend Hert": ["Lagerwey", "L82", "Rouveen", 52.59131, 6.22014, 9751, dt.datetime(2018, 9, 15), 5000000]
}

# Format:
# Id: [Name, Unit Of Measurement, Device Class, Timeframe Type]
PRODUCTION_SENSOR_TYPES = {
    "yeartotal": ["Production Year Total", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "YEAR3_YEARS"],
    "monthtotal": ["Production Month Total", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "YEAR_MONTHS"],
    "weektotal": ["Production Week Total", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "WEEK4_WEEKS"],
    "daytotal": ["Production Day Total", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "MONTH_DAYS"],
    "yearshares": ["Production Year Shares", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "YEAR3_YEARS"],
    "monthshares": ["Production Month Shares", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "YEAR_MONTHS"],
    "weekshares": ["Production Week Shares", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "WEEK4_WEEKS"],
    "dayshares": ["Production Day Shares", ENERGY_KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "MONTH_DAYS"]
}

class powerProducer: 
    def __init__(self, windturbine_name, windturbine_code, windturbine_shares) -> None:
        self.name = windturbine_name
        self.code = windturbine_code
        self.shares = windturbine_shares

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'code': self.code,
            'shares': self.shares
        }