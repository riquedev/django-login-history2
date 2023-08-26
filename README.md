# django-login-history2

![GitHub License](https://img.shields.io/github/license/riquedev/django-login-history2)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Django Version](https://img.shields.io/badge/django-3.2%2B-green)
![Maintenance](https://img.shields.io/maintenance/yes/2023)

**django-login-history2** is an enhanced version of the "[django-login-history](https://github.com/Dolidodzik/django-login-history)" package, 
providing a simple and effective way to track user login history in a Django project.

## Features

- Everything the previous package did
- Support maintained
- We use ipware instead of ipaddress

## Installation

Install **django-login-history2** using pip:

```bash
pip install django-login-history2
```

Add 'login_history' to your INSTALLED_APPS in the Django configuration file (settings.py):

```python
INSTALLED_APPS = [
    # ...
    'django_login_history2',
    # ...
]
```

Run migrations to create the required database tables:

```bash
python manage.py migrate
```

## Usage
django-login-history2 is easy to use. It will start automatically recording login history once installed and configured.