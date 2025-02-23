import abc

import requests
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from ipware import get_client_ip

from django_login_history2.dto import IPInfo


class IPCheckerAbstract(abc.ABC):
    __request: HttpRequest
    __client_ip: str
    __is_routable: bool
    __user : User
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
        return IPInfo(
            user=self.user.pk,
            ip=self.client_ip,
            user_agent=self.user_agent,
        )


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

    def get_geolocation_data(self) -> IPInfo:
        from django_login_history2.app_settings import get_cache, CACHE_TIMEOUT
        key = f'ipapi:{self.client_ip}'
        data = get_cache().get(key)

        if not data:
            data = super().get_geolocation_data()
            if not self.is_routable:
                data = data.with_overrides(error=True, reason="Address not routable")
            else:
                with requests.get(f'https://ipapi.co/{self.client_ip}/json/') as handler:
                    data = data.with_overrides(**handler.json())

            get_cache().set(key, data, timeout=CACHE_TIMEOUT)

        return data
