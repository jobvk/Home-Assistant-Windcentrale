import logging
import json
import requests
from http import HTTPStatus
from datetime import timedelta
from defusedxml import ElementTree
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.util import dt as dt_util
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_SHOW_ON_MAP, CONF_SCAN_INTERVAL
from .const import *

_LOGGER = logging.getLogger(__name__)

class Wind:
    """Create Wind and windturbines and collect all data form config entry"""
    def __init__(self, hass, config_entry):
        self.config_entry = config_entry
        self.hass = hass
        self.id = DOMAIN

        self.windCredentials = Credentials(self.hass, self.config_entry.data[CONF_EMAIL], self.config_entry.data[CONF_PASSWORD])

        self.live = self.config_entry.options.get(CONF_OPTIONS_LIVE, DEFAULT_LIVE)
        self.live_interval = timedelta(seconds=self.config_entry.options.get(CONF_OPTIONS_LIVE_INTERVAL, DEFAULT_LIVE_INTERVAL))

        self.production = self.config_entry.options.get(CONF_OPTIONS_PRODUCTION, DEFAULT_PRODUCTION)
        self.production_interval = timedelta(minutes=self.config_entry.options.get(CONF_OPTIONS_PRODUCTION_INTERVAL, DEFAULT_PRODUCTION_INTERVAL))

        self.news = self.config_entry.options.get(CONF_OPTIONS_NEWS, DEFAULT_NEWS)
        self.news_filter = self.config_entry.options.get(CONF_OPTIONS_NEWS_FILTER, DEFAULT_NEWS_FILTER)
        self.news_interval = timedelta(minutes=self.config_entry.options.get(CONF_OPTIONS_NEWS_INTERVAL, DEFAULT_NEWS_INTERVAL))

        self.show_on_map = self.config_entry.options.get(CONF_SHOW_ON_MAP, DEFAULT_SHOW_ON_MAP)

        self.windturbines = []
        for windturbine in WINDTURBINES_LIST:
            if self.config_entry.data[windturbine] >= 1:
                self.windturbines.append(Windturbine(self, self.hass, windturbine, self.config_entry.data[windturbine]))

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
    def __init__(self, wind, hass, windturbine_name, windturbine_shares):
        self.wind = wind
        self.hass = hass
        self.name = windturbine_name
        self.shares = windturbine_shares
        self.id = WINDTURBINES_LIST[windturbine_name][0]
        self.manufacturer = WINDTURBINES_LIST[windturbine_name][1]
        self.model = WINDTURBINES_LIST[windturbine_name][2]
        self.location = WINDTURBINES_LIST[windturbine_name][3]
        self.latitude = WINDTURBINES_LIST[windturbine_name][4]
        self.longitude = WINDTURBINES_LIST[windturbine_name][5]
        self.startDate = WINDTURBINES_LIST[windturbine_name][6]
        self.liveapi = LiveAPI(self.hass, self.id, self.name)
        self.productionapi = ProductionAPI(self.hass, self.name, self.id, self.shares)
    
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
    def __init__(self, hass, windturbineId, windturbineName):
        self.hass = hass
        self.windturbine_id = windturbineId
        self.windturbine_name = windturbineName
        self.status = None
        self.response_data = {}
        self.main_url = "https://zep-api.windcentrale.nl/production"

    def __get_data(self):
        "Collect data form url"
        get_url = '{}/{}/{}'.format(self.main_url, self.windturbine_id, "live")
        return requests.get(get_url, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Updating live data of windturbine {} using Rest API'.format(self.windturbine_name))

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
    def __init__(self, hass, name, windturbineId, shares):
        self.hass = hass
        self.windturbine_name = name
        self.windturbine_id = windturbineId
        self.windturbine_shares = shares
        self.status = None
        self.winddelen = None
        self.response_data = {}
        self.value_data = {}
        self.main_url = "https://zep-api.windcentrale.nl/production/"

    def __get_data(self):
        "Collect data form url"
        get_url = '{}/{}'.format(self.main_url, self.windturbine_id)
        return requests.get(get_url, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Updating production data of windturbine {} using Rest API'.format(self.windturbine_name))

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
        self.windturbines_ids = []
        self.status = None
        self.main_url = "https://zep-api.windcentrale.nl/app/config"
        for windturbine in windturbines:
            self.windturbines_ids.append(windturbine.id)

    def __get_data(self):
        "Collect data form url"
        return requests.get(self.main_url, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Updating news data sensor')

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
                    if Windturbine_id == 0 or Windturbine_id in self.windturbines_ids:
                        response_data_list.append(value_data)
                elif self.news_filter == NEWS_FILTER[2]:
                    if Windturbine_id in self.windturbines_ids:
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

class Credentials:
    "Collect windshares data"
    def __init__(self, hass, email, password):
        self.hass = hass
        self.email = email
        self.password = password
        self.credentailsData = {'client_id': 'clientapp', 'client_secret': 123456, 'grant_type': 'password', 'password': self.password, 'scope': 'read write', 'username': self.email} 
        self.token_url = "https://zep-api.windcentrale.nl/oauth/token"
        self.persons_url = "https://zep-api.windcentrale.nl/persons"

    def __get_data_token(self):
        "Collect aouth token form url"
        credentailsHeaders = {'Authorization':'Basic Y2xpZW50YXBwOjEyMzQ1Ng=='}
        return requests.post(self.token_url, data=self.credentailsData, headers=credentailsHeaders, verify=True)

    def __get_data_persons(self):
        "Collect data form persons url"
        personsHeaders = {'Authorization':str(self.signin_data['token_type'] + " " + self.signin_data['access_token'])}
        return requests.get(self.persons_url, headers=personsHeaders, verify=True)

    async def test_credentails(self):
        _LOGGER.info('Testing if credentails are correct')
        try:
            result_data_credentials = await self.hass.async_add_executor_job(self.__get_data_token)
            self.signin_data = result_data_credentials.json()
            _LOGGER.info(self.signin_data)
            if result_data_credentials.status_code == HTTPStatus.OK:
                return 'succes'
            elif result_data_credentials.status_code == HTTPStatus.BAD_REQUEST:
                if self.signin_data["error"] == "invalid_grant":
                    return self.signin_data['error_description']
            else:
                _LOGGER.error("Error while testing credentials: {}".format(self.signin_data))
                return 'error'

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server when testing credentails')
            return 'error'

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching testing credentails: %r', exc)
            return 'error'
    
    async def collect_windshares(self):
        _LOGGER.info('Colllecting windshares')
        try:
            result_data_persons = await self.hass.async_add_executor_job(self.__get_data_persons)
            persons_data = result_data_persons.json()
            _LOGGER.info(persons_data)
            if result_data_persons.status_code == HTTPStatus.OK:

                powerproducer_list = []
                firstPowerProducer = persons_data["shares"][0]["address"]["shares"][1]["powerProducer"]
                powerproducer_list.append(powerProducer(firstPowerProducer["@id"], firstPowerProducer["millId"], firstPowerProducer["name"]))
                for windturbine in persons_data["shares"][0]["address"]["shares"][1]["powerProducer"]["energySupplier"]["powerProducers"]:
                    if (('@id' in windturbine) and (windturbine["millId"] != 0)):
                        powerproducer_list.append(powerProducer(windturbine["@id"], windturbine["millId"], windturbine["name"]))

                ShareList = []
                ShareList.append(Shares(persons_data["shares"][0]["@id"], persons_data["shares"][0]["powerProducer"]["@ref"]))
                ShareList.append(Shares(persons_data["shares"][0]["address"]["shares"][1]["@id"], persons_data["shares"][0]["address"]["shares"][1]["powerProducer"]["@id"]))
                for shares in persons_data["shares"][0]["address"]["shares"][2:]:
                    if (('@id' in shares) and ('powerProducer' in shares)):
                        ShareList.append(Shares(shares["@id"], shares["powerProducer"]["@ref"]))

                for windproducer in powerproducer_list:
                    for share in ShareList:
                        if(windproducer.id == share.powerProducer):
                            windproducer.add_shares()

                windshares = {}

                for powerproducer in powerproducer_list:
                    windshares[powerproducer.name] = { "id" : powerproducer.id, "windturbine_id" : powerproducer.windturbine_id, "shares" : powerproducer.shares }

                _LOGGER.info(windshares)

                return windshares
            else:
                _LOGGER.error("Error while collecting windshares: {}".format(persons_data))
                return None

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server when testing credentails')
            return None

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching testing credentails: %r', exc)
            return None