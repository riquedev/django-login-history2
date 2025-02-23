import abc
from django.http import HttpRequest
from ipware import get_client_ip

from django_login_history2.dto import IPInfo


class IPCheckerAbstract(abc.ABC):
    __request: HttpRequest
    __client_ip: str
    __is_routable: bool

    def __init__(self, request: HttpRequest):
        self.__request = request
        self.__client_ip, self.__is_routable = get_client_ip(request)

    @property
    def client_ip(self) -> str:
        return self.__client_ip

    @property
    def is_routable(self) -> bool:
        return self.__is_routable

    @abc.abstractmethod
    def get_geolocation_data(self) -> IPInfo:
        pass
