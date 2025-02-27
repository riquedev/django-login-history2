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
- LOGIN_HISTORY_GEOLOCATION_HELPER_CLASS: Define the class used for geolocation (Default: django_login_history2.helper.IPCheckerIPApi).
- LOGIN_HISTORY_GEOLOCATION_PLACEHOLDER_IP: Define a placeholder IP for testing mode (Default: 8.8.8.8).
- LOGIN_HISTORY_GEOLOCATION_CACHE: Specify the cache to use for geolocation data.
- LOGIN_HISTORY_IP_API_KEY: Define the API Key used by IP API Service class (paid plans)

## Usage
Once installed and configured, __django-login-history2__ will automatically start recording login and logout events for all users.

To access the login history for a user, you can use the __login_history__ related field:

```python
user = User.objects.get(username="myuser")
history = user.login_history.all()
```

# IP Geolocation Provider Extension

This module allows you to extend the functionality of the `IPChecker` class by adding custom providers to fetch geolocation data for IP addresses. The provided example shows how to implement a new provider by creating a class that extends the `IPCheckerAbstract` class and implements the `get_geolocation_data()` method.

## How to Create a New Geolocation Provider

To create your own IP geolocation provider, follow these steps:

### 1. Create a New Class That Inherits from `IPCheckerAbstract`

Your class should inherit from `IPCheckerAbstract` to ensure it has all the required properties and methods for retrieving geolocation data for an IP address.

### 2. Implement the `get_geolocation_data()` Method

The `get_geolocation_data()` method should be implemented to fetch the geolocation data either from an external service or a custom logic.

#### Example: `MyIPService` Provider

```python
import requests
from django_login_history2.app_settings import get_cache, CACHE_TIMEOUT
from django_login_history2.helper import IPCheckerAbstract, IPInfo
class IPCheckerMyIPService(IPCheckerAbstract):
    def get_geolocation_data(self) -> IPInfo:        
        key = f'myipservice:{self.client_ip}'
        data = get_cache().get(key)

        if not data:
            data = super().get_geolocation_data()
            if not self.is_routable:
                data = data.with_overrides(error=True, reason="Address not routable")
            else:                
                response = requests.get(f'https://myipservice.com/{self.client_ip}/json/', timeout=60)
                geolocation_data = response.json()
                data = data.with_overrides(**geolocation_data)            
            get_cache().set(key, data, timeout=CACHE_TIMEOUT)

        return data
```
### 3. Register Your New Provider
To use your custom provider, register it in the appropriate part of your code or configuration. This ensures that your provider is used to fetch the geolocation data when necessary.

#### Key Concepts
- Cache: To avoid making repetitive calls to external APIs, the get_cache() function is used to cache geolocation data. This improves performance and reduces external service dependencies.
- Timeout and Error Handling: External APIs may have slow responses or return errors, so it's important to add error handling and set appropriate timeouts, as shown in the example.
- Custom Data: The get_geolocation_data() method can return more than just basic geolocation information, such as country, city, coordinates (latitude/longitude), etc. You can also customize it to return an error if the IP address is not routable.

### Example Usage
Once you have implemented and registered your custom provider, you can use it in your code like so:

```python
ip_checker = IPCheckerMyIPService(request, user)
geolocation_data = ip_checker.get_geolocation_data()
print(geolocation_data)
```

## Contributing
Feel free to open issues or create pull requests to contribute to the project. If you find a bug or need a feature, open an issue and we will try to fix it as soon as possible.

License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.