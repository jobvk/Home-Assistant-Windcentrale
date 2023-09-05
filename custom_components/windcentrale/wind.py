import logging
import json
import requests
import boto3
import datetime
from pycognito.aws_srp import AWSSRP
from http import HTTPStatus
from datetime import timedelta
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.util import dt as dt_util
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_PLATFORM, CONF_SHOW_ON_MAP
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
        self.base_url = self.get_base_url()
        self.credentialsapi = Credentials(self.hass, self.config_entry.data[CONF_EMAIL], self.config_entry.data[CONF_PASSWORD], self.config_entry.data[CONF_PLATFORM])

        self.windturbines = []
        for windturbine in self.config_entry.data[CONF_WINDTUBINES]:
            self.windturbines.append(Windturbine(self, self.hass, windturbine["name"], windturbine["code"], windturbine["shares"]))

        self.newsapi = NewsAPI(self, self.hass)

    @property
    def news_data(self):
        "Set news data form news api result"
        return self.newsapi.response_data

    async def update_windturbines(self):
        "Update windturbines after button press"
        _LOGGER.info('Update windshares')

        # Create a copy of the existing data
        config_entry_data = dict(self.config_entry.data)

        config_entry_data[CONF_WINDTUBINES] = []
        result_projects_windshares = await self.credentialsapi.collect_projects_windshares()
        for windturbine in result_projects_windshares.keys():
            config_entry_data[CONF_WINDTUBINES].append(result_projects_windshares[windturbine].to_dict())

        # Assign the updated data back to the config_entry
        self.config_entry.data = config_entry_data

        for windturbine_name in WINDTURBINES_LIST:
            found_in_self_windturbines = False
            for windturbine in self.windturbines:
                if windturbine.name == windturbine_name:
                    found_in_self_windturbines = True
                    break
            
            for config_windturbine in self.config_entry.data[CONF_WINDTUBINES]:
                if windturbine_name == config_windturbine["name"]:
                    if found_in_self_windturbines:
                        # Update the wind turbine
                        for windturbine in self.windturbines:
                            if windturbine.name == windturbine_name:
                                index = self.windturbines.index(windturbine)
                                _LOGGER.info('Update the shares of windturbine {} from {} to {} shares'.format(windturbine_name, self.windturbines[index].shares, config_windturbine["shares"]))
                                self.windturbines[index].shares = config_windturbine["shares"]
                                break
                    else:
                        # Add the wind turbine to self.windturbines
                        _LOGGER.info('Add windturbine {} with {} shares'.format(windturbine_name, config_windturbine["shares"]))
                        self.windturbines.append(Windturbine(self, self.hass, config_windturbine["name"], config_windturbine["code"], config_windturbine["shares"]))
                else:
                    # Delete the wind turbine from self.windturbines
                    if found_in_self_windturbines:
                        _LOGGER.info('Delete windturbine {}'.format(windturbine_name))
                        for windturbine in self.windturbines:
                            if windturbine.name == windturbine_name:
                                windturbine.cancel_scheduled_updates()
                                self.hass.add_job(self.async_remove_device, windturbine.id)
                        self.windturbines = [windturbine for windturbine in self.windturbines if windturbine.name != windturbine_name]
        self.hass.config_entries.async_update_entry(self.config_entry, data=self.config_entry.data)
        await self.hass.config_entries.async_reload(self.config_entry.entry_id)

    @callback
    def async_remove_device(self, device_id: str) -> None:
        """Remove device from Home Assistant."""
        _LOGGER.info("Remove device: %s", device_id)
        device_registry = dr.async_get(self.hass)
        device_entry = device_registry.async_get_device(
            identifiers={(DOMAIN, device_id)}
        )
        if device_entry is not None:
            device_registry.async_remove_device(device_entry.id)

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

    async def update_token_now(self):
        self.tokens = await self.credentialsapi.authenticate_user_credentails()

    def get_base_url(self):
        platform = self.config_entry.data[CONF_PLATFORM]
        if platform == "Windcentrale":
            return WINDCENTRALE_BASE_URL
        elif platform == "Winddelen":
            return WINDDELEN_BASE_URL

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
        self.live_update_task = None
        self.production_windtrubine_year_api = ProductionAPI(self.hass, self.wind, self.id, self.name, "YEAR3_YEARS", 0, "TOTAL_PROJECT")
        self.production_windtrubine_month_api = ProductionAPI(self.hass, self.wind, self.id, self.name, "YEAR_MONTHS", 0, "TOTAL_PROJECT")
        self.production_windtrubine_week_api = ProductionAPI(self.hass, self.wind, self.id, self.name, "WEEK4_WEEKS", 0, "TOTAL_PROJECT")
        self.production_shares_year_api = ProductionAPI(self.hass, self.wind, self.id, self.name, "YEAR3_YEARS", 0, "SHARES_IN_PROJECT")
        self.production_shares_month_api = ProductionAPI(self.hass, self.wind, self.id, self.name, "YEAR_MONTHS", 0, "SHARES_IN_PROJECT")
        self.production_shares_week_api = ProductionAPI(self.hass, self.wind, self.id, self.name, "WEEK4_WEEKS", 0, "SHARES_IN_PROJECT")
        self.production_update_task = None

    @property
    def live_data(self):
        "Set live data form live api result"
        return self.liveapi.response_data

    @property
    def production_windtrubine_year_data(self):
        "Set production data form production api result"
        return self.production_windtrubine_year_api.response_data

    @property
    def production_windtrubine_month_data(self):
        "Set production data form production api result"
        return self.production_windtrubine_month_api.response_data

    @property
    def production_windtrubine_week_data(self):
        "Set production data form production api result"
        return self.production_windtrubine_week_api.response_data

    @property
    def production_shares_year_data(self):
        "Set production data form production api result"
        return self.production_shares_year_api.response_data

    @property
    def production_shares_month_data(self):
        "Set production data form production api result"
        return self.production_shares_month_api.response_data

    @property
    def production_shares_week_data(self):
        "Set production data form production api result"
        return self.production_shares_week_api.response_data

    @property
    def show_on_map(self):
        "Return if the windturbine has to be shown on the map"
        return self.wind.show_on_map

    async def schedule_update_live(self, interval):
        "Schedule update based on live interval"
        nxt = dt_util.utcnow() + interval
        self.live_update_task = async_track_point_in_utc_time(self.hass, self.async_update_live, nxt)

    async def async_update_live(self, *_):
        "Start update and schedule update based on live interval"
        await self.liveapi.update()
        await self.schedule_update_live(timedelta(minutes=LIVE_INTERVAL))

    async def schedule_update_production(self, interval):
        "Schedule update based on production interval"
        nxt = dt_util.utcnow() + interval
        self.production_update_task = async_track_point_in_utc_time(self.hass, self.async_update_production, nxt)

    async def async_update_production(self, *_):
        "Start update and schedule update based on production interval"
        await self.production_windtrubine_year_api.update()
        await self.production_windtrubine_month_api.update()
        await self.production_windtrubine_week_api.update()
        await self.production_shares_year_api.update()
        await self.production_shares_month_api.update()
        await self.production_shares_week_api.update()
        await self.schedule_update_production(timedelta(hours=PRODUCTION_INTERVAL))

    def cancel_scheduled_updates(self):
        "Cancel scheduled live and production updates"
        if self.live_update_task:
            self.live_update_task()
            self.live_update_task = None

        if self.production_update_task:
            self.production_update_task()
            self.production_update_task = None

class LiveAPI:
    "Collect live data"
    def __init__(self, hass, wind, windturbineId, windturbineName):
        self.hass = hass
        self.wind = wind
        self.windturbine_id = windturbineId
        self.windturbine_name = windturbineName
        self.response_data = {}

    def __get_data(self):
        "Collect data form url"
        get_url = 'https://{}/api/v0/livedata?projects={}'.format(self.wind.base_url, self.windturbine_id)
        return requests.get(get_url, headers=self.wind.tokens, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Collecting live data of windturbine {}'.format(self.windturbine_name))

        try:
            if self.wind.tokens is None:
                return

            request_data = await self.hass.async_add_executor_job(self.__get_data)
            
            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.warning('Invalid response from server when collecting live data of windturbine {} with the response data {} and status code {}'.format(self.windturbine_name, request_data.text, request_data.status_code))
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

        except Exception as exc:
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            return


class ProductionAPI:
    "Collect production data"
    def __init__(self, hass, wind, windturbineId, windturbineName, timeframeType, timeframeOffset, viewType):
        self.hass = hass
        self.wind = wind
        self.windturbine_id = windturbineId
        self.windturbine_name = windturbineName
        self.timeframe_type = timeframeType
        self.timeframe_offset = timeframeOffset
        self.view_type = viewType
        self.response_data = {}

    def __get_data(self):
        "Collect data form url"
        get_url = 'https://{}/api/v0/sustainable/production/{}?timeframe_type={}&timeframe_offset={}&view_type={}'.format(self.wind.base_url, self.windturbine_id, self.timeframe_type, self.timeframe_offset, self.view_type)
        return requests.get(get_url, headers=self.wind.tokens, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Collecting production data of windturbine {} with view_type: {}, timeframe_type: {}'.format(self.windturbine_name, self.view_type, self.timeframe_type))

        try:
            if self.wind.tokens is None:
                return
            
            request_data = await self.hass.async_add_executor_job(self.__get_data)

            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.warning('Invalid response from server when collecting production data with the response data {} and status code {}'.format(request_data.text, request_data.status_code))
                return

            self.response_data.clear()
            json_items = json.loads(json.dumps(request_data.json()))

            for json_item in json_items:

                if self.timeframe_type == "YEAR3_YEARS":
                    date_object = json_item["labels"]["year"]
                elif self.timeframe_type == "YEAR_MONTHS":
                    date_object = json_item["labels"]["month"]
                elif self.timeframe_type == "WEEK4_WEEKS":
                    date_object = json_item["labels"]["week"]

                value = json_item["value"]

                self.response_data[date_object] = value

        except requests.exceptions.Timeout:
            _LOGGER.error('Timeout response from server for collection production data for windturbine {}'.format(self.windturbine_name))
            return
        except Exception as exc:
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            return

class NewsAPI:
    "Collect news data"
    def __init__(self, wind, hass):
        self.wind = wind
        self.hass = hass
        self.response_data = ""

    def __get_data(self):
        "Collect data form url"
        get_url = 'https://{}/api/v0/sustainable/notices'.format(self.wind.base_url)
        return requests.get(get_url, headers=self.wind.tokens, verify=True)

    async def update(self):
        "Get data ready for home assitant"
        _LOGGER.info('Collecting news data sensor')

        try:
            if self.wind.tokens is None:
                return

            request_data = await self.hass.async_add_executor_job(self.__get_data)

            if not request_data.status_code == HTTPStatus.OK:
                _LOGGER.warning('Invalid response from server when collecting news data with the response data {} and status code {}'.format(request_data.text, request_data.status_code))
                return

            self.response_data = ""
            json_items = json.loads(json.dumps(request_data.json()))
            news_item = json_items[0]
            publication_date = datetime.datetime.fromisoformat(news_item['publication_date_time']).strftime("%d-%m-%Y %H:%M:%S")
            self.response_data = "{}\n---------\n{}\n\nPublicatiedatum: {}".format(news_item['title'], news_item['message'], publication_date)

        except requests.exceptions.Timeout:
            _LOGGER.error('Timeout response from server for collection news data')
            return
        except Exception as exc:
            _LOGGER.error('While fetching the news data an error occurred: {}'.format(exc))
            return

class Credentials:
    "Checking credentials & collecting windturbines of which you own shares"
    def __init__(self, hass, email, password, platform):
        self.hass = hass
        self.email = email
        self.password = password
        self.platform = platform
        self.authorization_header = None
        self.projects_list = None

    def __get_tokens(self):
        boto3_client = boto3.client('cognito-idp', region_name='eu-west-1')
        if self.platform == "Windcentrale":
            pool_id = WINDCENTRALE_POOL_ID
            client_id = WINDCENTRALE_CLIENT_ID
        elif self.platform == "Winddelen":
            pool_id = WINDDELEN_POOL_ID
            client_id = WINDDELEN_CLIENT_ID
        aws = AWSSRP(username=self.email, password=self.password, pool_id=pool_id, client_id=client_id, client=boto3_client)
        return aws.authenticate_user()

    def __get_projects(self):
        "Collect windturbine's form projects url"
        if self.platform == "Windcentrale":
            base_url = WINDCENTRALE_BASE_URL
        elif self.platform == "Winddelen":
            base_url = WINDDELEN_BASE_URL
        get_url = 'https://{}/api/v0/sustainable/projects'.format(base_url)
        return requests.get(get_url, headers=self.authorization_header, verify=True)

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
        _LOGGER.info('Collecting windturbines shares')
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
                _LOGGER.error("HTTP status code was not 200 while collecting windturbines shares, Result: %r", result_projects)
                return None

        except requests.exceptions.Timeout:
            _LOGGER.error('Timeout response from server when collecting windturbines of which you own shares')
            return None

        except Exception as exc:
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            return None