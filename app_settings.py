from django.conf import settings


GEOLOCATION_METHOD = getattr(
    settings,
    'LOGIN_HISTORY_GEOLOCATION_METHOD',
    'django_login_history2.utils.get_geolocation_data'
)

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

DEBUG = getattr(settings, 'DEBUG', True)