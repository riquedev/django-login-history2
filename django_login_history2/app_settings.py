import importlib
import sys
from typing import Type
from django.conf import settings
from django.core.cache import caches
from django.core.cache.backends.base import BaseCache
from django_login_history2.helper import IPCheckerAbstract

IS_TESTING = sys.argv[1:2] == ['test']

GEOLOCATION_METHOD = getattr(
    settings,
    'LOGIN_HISTORY_GEOLOCATION_METHOD',
    'django_login_history2.utils.get_geolocation_data'
)

GEOLOCATION_HELPER_CLASS = getattr(
    settings,
    'LOGIN_HISTORY_GEOLOCATION_HELPER_CLASS',
    'django_login_history2.helper.IPCheckerIPApi'
)

def get_geolocation_helper_class() -> Type[IPCheckerAbstract]:
    module_name, class_name = GEOLOCATION_HELPER_CLASS.rsplit('.', 1)
    try:

        if IS_TESTING:
            class_name = 'IPCheckerTestMode'

        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as er:
        raise ValueError("Invalid geolocation class specified in settings.\n", er) from er



GEOLOCATION_BLOCK_FIELDS = (
    'user',
    'ip',
    'user_agent',
    'ip_info',
    'created_at'
)

GEOLOCATION_PLACEHOLDER_IP = getattr(
    settings,
    'LOGIN_HISTORY_GEOLOCATION_PLACEHOLDER_IP',
    '8.8.8.8'
)

CACHE = getattr(
    settings,
    'LOGIN_HISTORY_GEOLOCATION_CACHE',
    'default'
)

CACHE_TIMEOUT = getattr(
    settings,
    'LOGIN_HISTORY_GEOLOCATION_CACHE_TIMEOUT',
    3600
)

def get_cache() -> BaseCache:
    return caches[CACHE]

DEBUG = getattr(settings, 'DEBUG', True)
