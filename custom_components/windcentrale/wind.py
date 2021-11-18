from http import HTTPStatus
import logging
import json
import requests
from datetime import timedelta
from defusedxml import ElementTree
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.util import dt as dt_util
from homeassistant.const import CONF_SHOW_ON_MAP, CONF_SCAN_INTERVAL
from .const import *

_LOGGER = logging.getLogger(__name__)

class Wind:
    """Create Wind and windturbines and collect all data form config entry"""
    def __init__(self, hass, config_entry):
        self.config_entry = config_entry
        self.hass = hass
        self.id = DOMAIN

        self.live = self.config_entry.options.get(CONF_OPTIONS_LIVE, DEFAULT_LIVE)
        self.live_interval = timedelta(seconds=self.config_entry.options.get(CONF_OPTIONS_LIVE_INTERVAL, DEFAULT_LIVE_INTERVAL))

        self.production = self.config_entry.options.get(CONF_OPTIONS_PRODUCTION, DEFAULT_PRODUCTION)
        self.production_interval = timedelta(minutes=self.config_entry.options.get(CONF_OPTIONS_PRODUCTION_INTERVAL, DEFAULT_PRODUCTION_INTERVAL))

        self.news = self.config_entry.options.get(CONF_OPTIONS_NEWS, DEFAULT_NEWS)
        self.news_filter = self.config_entry.options.get(CONF_OPTIONS_NEWS_FILTER, DEFAULT_NEWS_FILTER)
        self.news_interval = timedelta(minutes=self.config_entry.options.get(CONF_OPTIONS_NEWS_INTERVAL, DEFAULT_NEWS_INTERVAL))

        self.show_on_map = self.config_entry.options.get(CONF_SHOW_ON_MAP, DEFAULT_SHOW_ON_MAP)

        self.windturbines = []
        for windturbineitem in WINDTURBINES_LIST:
            if self.config_entry.data[WINDTURBINES_LIST[windturbineitem][0]] >= 1:
                self.windturbines.append(Windturbine(self.hass, windturbineitem, self))

        self.newsapi = NewsAPI(self.hass, self.news_filter, self.windturbines)

    @property
    def wind_id(self):
        "Wind id equals to domain"
        return self.id

    @property
    def news_status(self):
        "Set news status as result of api"
        return self.newsapi.status

    @property
    def news_data(self):
        "Set news data form news api result"
        return self.newsapi.response_data

    async def schedule_update_news(self, interval):
        "Schedule update based on news interval"
        nxt = dt_util.utcnow() + interval
        async_track_point_in_utc_time(self.hass, self.async_update_news, nxt)

    async def async_update_news(self, *_):
        "Start update and schedule update based on news interval"
        await self.newsapi.update()
        await self.schedule_update_news(self.news_interval)

class Windturbine:
    "Create windturbine and collect data"
    def __init__(self, hass, windturbineitem, wind):
        self.hass = hass
        self.wind = wind
        self.id = WINDTURBINES_LIST[windturbineitem][0]
        self.name = WINDTURBINES_LIST[windturbineitem][1]
        self.number = WINDTURBINES_LIST[windturbineitem][2]
        self.manufacturer = WINDTURBINES_LIST[windturbineitem][3]
        self.model = WINDTURBINES_LIST[windturbineitem][4]
        self.location = WINDTURBINES_LIST[windturbineitem][5]
        self.latitude = WINDTURBINES_LIST[windturbineitem][6]
        self.longitude = WINDTURBINES_LIST[windturbineitem][7]
        self.startDate = WINDTURBINES_LIST[windturbineitem][8]
        self.shares = self.wind.config_entry.data[self.id]
        self.liveapi = LiveAPI(self.hass, self.name, self.number)
        self.productionapi = ProductionAPI(self.hass, self.name, self.number, self.shares)
    
    @property
    def windturbine_id(self):
        "Set id of windturbine"
        return self.id

    @property
    def live_status(self):
        "Set live status as result of api"
        return self.liveapi.status

    @property
    def live_data(self):
        "Set live data form live api result"
        return self.liveapi.response_data

    @property
    def production_status(self):
        "Set production status as result of api"
        return self.productionapi.status

    @property
    def production_data(self):
        "Set production data form production api result"
        return self.productionapi.response_data

    @property
    def show_on_map(self):
        "Return if the windturbine has to be shown on the map"
        return self.wind.show_on_map

    async def schedule_update_live(self, interval):
        "Schedule update based on live interval"
        nxt = dt_util.utcnow() + interval
        async_track_point_in_utc_time(self.hass, self.async_update_live, nxt)

    async def async_update_live(self, *_):
        "Start update and schedule update based on live interval"
        await self.liveapi.update()
        await self.schedule_update_live(self.wind.live_interval)

    async def schedule_update_production(self, interval):
        "Schedule update based on production interval"
        nxt = dt_util.utcnow() + interval
        async_track_point_in_utc_time(self.hass, self.async_update_production, nxt)

    async def async_update_production(self, *_):
        "Start update and schedule update based on production interval"
        await self.productionapi.update()
        await self.schedule_update_production(self.wind.production_interval)

class LiveAPI:
    "Collect live data"
    def __init__(self, hass, name, number):
        self.hass = hass
        self.windturbine_name = name
        self.windturbine_number = number
        self.status = None
        self.response_data = {}
        self.main_url = "https://zep-api.windcentrale.nl/production"

    def __get_data(self):
        "Collect data form url"
        get_url = '{}/{}/{}'.format(self.main_url, self.windturbine_number, "live")
        return requests.get(get_url, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.debug('Updating live data of windturbine {} using Rest API'.format(self.windturbine_name))

        try:
            request_data = await self.hass.async_add_executor_job(self.__get_data)
            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.error('Invalid response from server for collection live data of windturbine {}'.format(self.windturbine_name))
                self.status = False
                return

            if request_data.text == "":
                _LOGGER.error('No live data found for windturbine {}'.format(self.windturbine_name))
                self.status = False
                return

            self.response_data.clear()

            json_file = request_data.json()
            json_dump = json.dumps(json_file)
            json_load = json.loads(json_dump)

            for key, value in json_load.items():
                if key == "powerAbsTot" or key == "powerAbsWd" or key == "kwhForecast" or key == "kwh" or key == "windSpeed" or key == "powerRel":
                    self.response_data[key] = int(value)
                elif key == "hoursRunThisYear" or key == "runPercentage":
                    self.response_data[key] = round(value, 2)
                else:
                    self.response_data[key] = value
            self.status = True

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server for collection history data for windturbine {}'.format(self.windturbine_name))
            self.status = False
            return

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            self.status = False
            return

class ProductionAPI:
    "Collect production data"
    def __init__(self, hass, name, number, shares):
        self.hass = hass
        self.windturbine_name = name
        self.windturbine_number = number
        self.windturbine_shares = shares
        self.status = None
        self.winddelen = None
        self.response_data = {}
        self.value_data = {}
        self.main_url = "https://zep-api.windcentrale.nl/production/"

    def __get_data(self):
        "Collect data form url"
        get_url = '{}/{}'.format(self.main_url, self.windturbine_number)
        return requests.get(get_url, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.debug('Updating production data of windturbine {} using Rest API'.format(self.windturbine_name))

        try:
            request_data = await self.hass.async_add_executor_job(self.__get_data)
            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.error('Invalid response from server for collection production data of windturbine {}'.format(self.windturbine_name))
                self.status = False
                return

            if request_data.text == "":
                _LOGGER.error('No production data found for windturbine {}'.format(self.windturbine_name))
                self.status = False
                return

            self.response_data.clear()
            root = ElementTree.fromstring(request_data.text)

            self.total_windshares = root[0].attrib.get('winddelen')

            for child in root[0]:
                value_data = {}
                value_data[0] = child.attrib.get('tstart')
                value_data[1] = child.attrib.get('tend')

                total_value = child.attrib.get('sum')
                value_one_share = float(total_value) / int(self.total_windshares)

                if child.attrib.get('period') == 'DAY':
                    value_all_shares = value_one_share * (self.windturbine_shares * 1000)
                    value_data[2] = round(value_all_shares, 1)
                elif child.attrib.get('period') == 'WEEK':
                    value_all_shares = value_one_share * self.windturbine_shares
                    value_data[2] = round(value_all_shares, 1)
                elif child.attrib.get('period') == 'MONTH':
                    value_all_shares = value_one_share * self.windturbine_shares
                    value_data[2] = round(value_all_shares, 2)
                elif child.attrib.get('period') == 'YEAR' or child.attrib.get('period') == 'LIFETIME':
                    value_all_shares = value_one_share * (self.windturbine_shares / 1000)
                    value_data[2] = round(value_all_shares, 3)
                self.response_data[child.attrib.get('period')] = value_data
            self.status = True

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server for collection production data for windturbine {}'.format(self.windturbine_name))
            self.status = False
            return

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            self.status = False
            return

class NewsAPI:
    "Collect news data"
    def __init__(self, hass, news_filter, windturbines):
        self.hass = hass
        self.news_filter = news_filter
        self.response_data = None
        self.windturbines_numbers = []
        self.status = None
        self.main_url = "https://zep-api.windcentrale.nl/app/config"
        for windturbine in windturbines:
            self.windturbines_numbers.append(windturbine.number)

    def __get_data(self):
        "Collect data form url"
        return requests.get(self.main_url, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.debug('Updating news data sensor')

        try:
            request_data = await self.hass.async_add_executor_job(self.__get_data)
            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.error('Invalid response from server for collection news data')
                self.status = False
                return

            if request_data.text == "":
                _LOGGER.error('No news data found')
                self.status = False
                return

            self.response_data = None
            response_data_list = []

            root = ElementTree.fromstring(request_data.text)
            for newsitems in root.findall('./news/'):
                value_data = {}
                value_data[0] = newsitems.attrib.get('id')
                value_data[1] = newsitems.attrib.get('i')
                value_data[2] = int(newsitems.attrib.get('m'))
                Windturbine_id = int(newsitems.attrib.get('m'))
                value_data[3] = newsitems.attrib.get('t')
                value_data[4] = newsitems.find('t').text
                value_data[5] = newsitems.find('c').text
                if self.news_filter == NEWS_FILTER[0]:
                    response_data_list.append(value_data)
                elif self.news_filter == NEWS_FILTER[1]:
                    if Windturbine_id == 0 or Windturbine_id in self.windturbines_numbers:
                        response_data_list.append(value_data)
                elif self.news_filter == NEWS_FILTER[2]:
                    if Windturbine_id in self.windturbines_numbers:
                        response_data_list.append(value_data)

            first_item = response_data_list[0]
            self.response_data = '{}\n---------\n{}\n\nPublicatiedatum: {}'.format(first_item[4], first_item[5], first_item[3])
            self.status = True

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server for collection news data')
            self.status = False
            return

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            self.status = False
            return