import requests
from functools import lru_cache
from django_login_history2.app_settings import CACHE_SIZE, IS_TESTING



@lru_cache(maxsize=CACHE_SIZE)
def get_geolocation_data(ip: str):
    with requests.get(f'https://ipapi.co/{ip}/json/') as handler:
        return handler.json()
