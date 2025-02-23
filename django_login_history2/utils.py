from django.contrib.auth.models import User
from django.http import HttpRequest
from django_login_history2.app_settings import get_geolocation_helper_class
from django_login_history2.dto import IPInfo


def get_geolocation_data(request: HttpRequest, user: User) -> IPInfo:
    cls = get_geolocation_helper_class()
    return cls(request, user).get_geolocation_data()
