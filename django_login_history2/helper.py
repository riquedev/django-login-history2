import abc

import requests
from django.contrib.auth.models import User
from django.http import HttpRequest
from ipware import get_client_ip

from django_login_history2.dto import IPInfo
from django_login_history2.logger import get_logger


class IPCheckerAbstract(abc.ABC):
    __request: HttpRequest
    __client_ip: str
    __is_routable: bool
    __user : User
    logger = get_logger()

    def __init__(self, request: HttpRequest, user: User):
        self.__request = request
        self.__client_ip, self.__is_routable = get_client_ip(request)
        self.__user = user

    @property
    def client_ip(self) -> str:
        return self.__client_ip

    @property
    def is_routable(self) -> bool:
        return self.__is_routable

    @property
    def user_agent(self) -> str:
        return self.__request.META.get('HTTP_USER_AGENT', '')

    @property
    def user(self):
        return self.__user

    @abc.abstractmethod
    def get_geolocation_data(self) -> IPInfo:
        from django_login_history2.app_settings import SHOW_USER_IP_ON_LOGGING
        log_msg = f"Building a geolocation data from user {self.user.pk}"

        if SHOW_USER_IP_ON_LOGGING:
            log_msg += f" with IP {self.client_ip}"

        self.logger.debug(log_msg)

        return IPInfo(
            user=self.user.pk,
            ip=self.client_ip,
            user_agent=self.user_agent,
        )

    def after_load_ip_info(self, data: IPInfo):
        if data.error:
            self.logger.error(f"Can't get ip info from user {self.user.pk}: {data.error_reason}")
        return data


class IPCheckerTestMode(IPCheckerAbstract):

    def get_geolocation_data(self) -> IPInfo:
        from django_login_history2.app_settings import GEOLOCATION_PLACEHOLDER_IP
        return super().get_geolocation_data().with_overrides(
            ip=GEOLOCATION_PLACEHOLDER_IP,
            network='8.8.8.0/24',
            version='IPv4',
            city='Mountain View',
            region='California',
            region_code='CA',
            country='US',
            country_code='US',
            country_name='United States',
            currency='USD',
            country_code_iso3='USA',
            country_capital='Washington',
            country_tld='.us',
            continent_code='NA',
            in_eu=False,
            postal='94043',
            latitude=37.42301,
            longitude=-122.083352,
            timezone='America/Los_Angeles',
            utc_offset="-0800",
            country_calling_code='+1',
            currency_name='Dollar',
            languages='en-US,es-US,haw,fr',
            country_area=9629091.0,
            country_population=327167434,
            asn='AS15169',
            org='GOOGLE'
        )


class IPCheckerIPApi(IPCheckerAbstract):

    @property
    def api_key(self):
        from django_login_history2.app_settings import IP_API_KEY
        return IP_API_KEY

    def __init__(self, request: HttpRequest, user: User):
        super().__init__(request, user)

        if not self.api_key:
            self.logger.warning('You are using the default class "IPCheckerIPApi" without a LOGIN_HISTORY_IP_API_KEY, '
                                'consider purchasing a plan at "https://ipapi.co/#pricing" to avoid limits')

    def get_url(self):
        url = f'https://ipapi.co/{self.client_ip}/json/'
        if self.api_key:
            url += f'?key={self.api_key}'
        return url

    def get_geolocation_data(self) -> IPInfo:
        from django_login_history2.app_settings import get_cache, CACHE_TIMEOUT
        key = f'ipapi:{self.client_ip}'
        data = get_cache().get(key)

        if not data:
            data = super().get_geolocation_data()
            if not self.is_routable:
                data = data.with_overrides(error=True, error_reason="Address not routable")
            else:
                with requests.get(self.get_url(), timeout=60) as handler:
                    if handler.status_code in (200,403,429):
                        response = handler.json()
                        message = response.pop('message', '')
                        reason = response.pop('reason', '')
                        data = data.with_overrides(**response)
                        data.error_reason = f"{reason} {message}".strip()

            get_cache().set(key, data, timeout=CACHE_TIMEOUT)

        return data
