import requests


def get_geolocation_data(ip: str):
    with requests.get(f'https://ipapi.co/{ip}/json/') as handler:
        return handler.json()