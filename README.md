# django-login-history2

![GitHub License](https://img.shields.io/github/license/riquedev/django-login-history2)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Django Version](https://img.shields.io/badge/django-3.2%2B-green)
![Maintenance](https://img.shields.io/maintenance/yes/2025)

**django-login-history2** is an enhanced version of the "[django-login-history](https://github.com/Dolidodzik/django-login-history)" package. It provides an easy and effective way to track user login history in a Django project, including information like IP address, user-agent, geolocation, and more.

## Features

- Tracks user login and logout history.
- Stores device data, such as IP address, user-agent, geolocation, etc.
- Built-in support for easy customization and extension.
- Can be easily integrated with your existing Django application.
- Test mode with dummy geolocation data for testing purposes.

## Installation

To install **django-login-history2**, simply run:

```bash
pip install django-login-history2
```

Then, add 'django_login_history2' to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    # ...
    'django_login_history2',
    # ...
]
```
Run migrations to create the necessary database tables:
```bash
python manage.py migrate
```

## Configuration
This app can be configured through settings.py. The following settings are available:

- LOGIN_HISTORY_GEOLOCATION_METHOD: Define the method to use for geolocation. (Default: django_login_history2.utils.get_geolocation_data)
- LOGIN_HISTORY_GEOLOCATION_HELPER_CLASS: Define the class used for geolocation (Default: django_login_history2.helper.IPCheckerTestMode).
- LOGIN_HISTORY_GEOLOCATION_PLACEHOLDER_IP: Define a placeholder IP for testing mode (Default: 8.8.8.8).
- LOGIN_HISTORY_GEOLOCATION_CACHE: Specify the cache to use for geolocation data.

## Usage
Once installed and configured, __django-login-history2__ will automatically start recording login and logout events for all users.

To access the login history for a user, you can use the __login_history__ related field:

```python
user = User.objects.get(username="myuser")
history = user.login_history.all()
```

## Contributing
Feel free to open issues or create pull requests to contribute to the project. If you find a bug or need a feature, open an issue and we will try to fix it as soon as possible.

License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.