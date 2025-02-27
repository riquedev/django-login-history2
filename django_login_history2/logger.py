import logging

LOGGER_NAME = 'django_login_history2'


def get_logger():
    return logging.getLogger(LOGGER_NAME)
