import logging
import json
import requests
import boto3
import datetime
from pycognito.aws_srp import AWSSRP
from http import HTTPStatus
from datetime import timedelta
from defusedxml import ElementTree
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.util import dt as dt_util
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_SHOW_ON_MAP
from .const import *

_LOGGER = logging.getLogger(__name__)

class Wind:
    """Create Wind and windturbines and collect all data form config entry"""
    def __init__(self, hass, config_entry):
        self.config_entry = config_entry
        self.hass = hass
        self.id = DOMAIN
        self.tokens = None
        self.show_on_map = self.config_entry.options.get(CONF_SHOW_ON_MAP, DEFAULT_SHOW_ON_MAP)
        self.credentialsapi = Credentials(self.hass, self.config_entry.data[CONF_EMAIL], self.config_entry.data[CONF_PASSWORD])

        self.windturbines = []
        for windturbine in WINDTURBINES_LIST:
            if self.config_entry.data[windturbine] is not None:
                project = json.loads(self.config_entry.data[windturbine])
                self.windturbines.append(Windturbine(self, self.hass, project["name"], project["code"], project["shares"]))
    
        self.newsapi = NewsAPI(self, self.hass)

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
        await self.schedule_update_news(timedelta(minutes=NEWS_INTERVAL))

    async def schedule_update_token(self, interval):
        "Schedule update based on token interval"
        nxt = dt_util.utcnow() + interval
        async_track_point_in_utc_time(self.hass, self.async_update_token, nxt)

    async def async_update_token(self, *_):
        "Start update and schedule update based on token interval"
        self.tokens = await self.credentialsapi.authenticate_user_credentails()
        await self.schedule_update_token(timedelta(minutes=TOKEN_INTERVAL))

class Windturbine:
    "Create windturbine and collect data"
    def __init__(self, wind, hass, windturbine_name, windturbine_code, windturbine_shares):
        self.wind = wind
        self.hass = hass
        self.name = windturbine_name
        self.id = windturbine_code
        self.shares = windturbine_shares
        self.manufacturer = WINDTURBINES_LIST[windturbine_name][0]
        self.model = WINDTURBINES_LIST[windturbine_name][1]
        self.location = WINDTURBINES_LIST[windturbine_name][2]
        self.latitude = WINDTURBINES_LIST[windturbine_name][3]
        self.longitude = WINDTURBINES_LIST[windturbine_name][4]
        self.total_shares = WINDTURBINES_LIST[windturbine_name][5]
        self.start_date = WINDTURBINES_LIST[windturbine_name][6]
        self.energy_prognoses = WINDTURBINES_LIST[windturbine_name][7]
        self.liveapi = LiveAPI(self.hass, self.wind, self.id, self.name)
        #self.productionapi = ProductionAPI(self.hass, self.name, self.id, self.shares)

    @property
    def live_data(self):
        "Set live data form live api result"
        return self.liveapi.response_data

    # @property
    # def production_status(self):
    #     "Set production status as result of api"
    #     return self.productionapi.status

    # @property
    # def production_data(self):
    #     "Set production data form production api result"
    #     return self.productionapi.response_data

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
        await self.schedule_update_live(timedelta(seconds=LIVE_INTERVAL))

    # async def schedule_update_production(self, interval):
    #     "Schedule update based on production interval"
    #     nxt = dt_util.utcnow() + interval
    #     async_track_point_in_utc_time(self.hass, self.async_update_production, nxt)

    # async def async_update_production(self, *_):
    #     "Start update and schedule update based on production interval"
    #     await self.productionapi.update()
    #     await self.schedule_update_production(timedelta(minutes=PRODUCTION_INTERVAL))

class LiveAPI:
    "Collect live data"
    def __init__(self, hass, wind, windturbineId, windturbineName):
        self.hass = hass
        self.wind = wind
        self.windturbine_id = windturbineId
        self.windturbine_name = windturbineName
        self.response_data = {}
        self.main_url = "https://mijn.windcentrale.nl/api/v0/livedata"

    def __get_data(self):
        "Collect data form url"
        get_url = '{}?projects={}'.format(self.main_url, self.windturbine_id)
        return requests.get(get_url, headers=self.wind.tokens, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Updating live data of windturbine {} using Rest API'.format(self.windturbine_name))

        try:
            if self.wind.tokens is None:
                return

            request_data = await self.hass.async_add_executor_job(self.__get_data)
            
            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.error('Invalid response from server for collection live data of windturbine {} the response data {} and code {}'.format(self.windturbine_name, request_data.text, request_data.status_code))
                return

            if request_data.text == "":
                _LOGGER.error('No live data found for windturbine {}'.format(self.windturbine_name))
                return

            self.response_data.clear()
            json_items = json.loads(json.dumps(request_data.json()))

            for key, value in json_items[self.windturbine_id].items():
                if key == "wind_power" or key == "power" or key == "power_per_share" or key == "power_percentage" or key == "year_production" or key == "total_runtime":
                    self.response_data[key] = int(value)
                elif key == "rpm" or key == "year_runtime":
                    self.response_data[key] = float(value)
                elif key == "timestamp":
                    self.response_data[key] = datetime.datetime.fromtimestamp(int(value))
                elif key == "pulsating":
                    if value == "1":
                        self.response_data[key] = True
                    else:
                        self.response_data[key] = False
                else:
                    self.response_data[key] = value

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server for collection history data for windturbine {}'.format(self.windturbine_name))
            return

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching data: %r', exc)
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
    def __init__(self, wind, hass):
        self.wind = wind
        self.hass = hass
        self.response_data = ""
        self.main_url = "https://mijn.windcentrale.nl/api/v0/sustainable/notices"

    def __get_data(self):
        "Collect data form url"
        return requests.get(self.main_url, headers=self.wind.tokens, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Updating news data sensor')

        try:
            if self.wind.tokens is None:
                return

            request_data = await self.hass.async_add_executor_job(self.__get_data)

            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.error('Invalid response from server for collection news data')
                return

            if request_data.text == "":
                _LOGGER.error('No news data found')
                return

            self.response_data = ""
            json_items = json.loads(json.dumps(request_data.json()))
            news_item = json_items[0]
            publication_date = datetime.datetime.fromisoformat(news_item['publication_date_time']).strftime("%d-%m-%Y %H:%M:%S")
            self.response_data = "{}\n---------\n{}\n\nPublicatiedatum: {}".format(news_item['title'], news_item['message'], publication_date)
            _LOGGER.error(self.response_data)

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server for collection news data')
            return

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            return

class Credentials:
    "Checking credentials & collecting windturbines of which you own shares"
    def __init__(self, hass, email, password):
        self.hass = hass
        self.email = email
        self.password = password
        self.authorization_header = None
        self.projects_list = None

    def __get_tokens(self):
        boto3_client = boto3.client('cognito-idp', region_name='eu-west-1')
        aws = AWSSRP(username=self.email, password=self.password, pool_id='eu-west-1_U7eYBPrBd', client_id='715j3r0trk7o8dqg3md57il7q0', client=boto3_client)
        return aws.authenticate_user()

    def __get_projects(self):
        "Collect windturbine's form projects url"
        return requests.get("https://mijn.windcentrale.nl/api/v0/sustainable/projects", headers=self.authorization_header, verify=True)

    async def authenticate_user_credentails(self):
        _LOGGER.info('Testing if user credentails are correct')
        try:
            tokens = await self.hass.async_add_executor_job(self.__get_tokens)
            token_type = tokens['AuthenticationResult']['TokenType']
            id_token = tokens['AuthenticationResult']['IdToken']
            self.authorization_header = {'Authorization':token_type + " " + id_token}
            return self.authorization_header
        except:
            return 'invalid_user_credentails'

    async def collect_projects_windshares(self):
        _LOGGER.info('Collecting windturbines of which you own shares')
        try:
            result_projects = await self.hass.async_add_executor_job(self.__get_projects)
            if result_projects.status_code == HTTPStatus.OK:
                self.projects_list = dict()
                for json_windturbine in result_projects.json():
                    shares = 0
                    for participation in json_windturbine["participations"]:
                        shares += participation["share"]
                    self.projects_list[json_windturbine["project_name"]] = powerProducer(json_windturbine["project_name"], json_windturbine["project_code"], shares)
                return self.projects_list
            else:
                _LOGGER.error("HTTP status code was not 200 while collecting windturbines of which you own shares, Result: %r", result_projects)
                return None

        except requests.exceptions.Timeout:
            """Time out error of server connection"""
            _LOGGER.error('Timeout response from server when collecting windturbines of which you own shares')
            return None

        except requests.exceptions.RequestException as exc:
            """Error of server RequestException"""
            _LOGGER.error('Error occurred while collecting windturbines of which you own shares: %r', exc)
            return None