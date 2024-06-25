import importlib
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import FieldDoesNotExist
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model
from ipware import get_client_ip
from .utils import get_geolocation_data
from .app_settings import (GEOLOCATION_METHOD, GEOLOCATION_BLOCK_FIELDS,
                           GEOLOCATION_PLACEHOLDER_IP)


class Login(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    ip = models.GenericIPAddressField(db_index=True)
    ip_info = models.JSONField(default=dict)
    city = models.CharField(max_length=80, blank=True)
    region = models.CharField(max_length=80, blank=True)
    region_code = models.CharField(max_length=10, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    country_name = models.CharField(max_length=80, blank=True)
    currency = models.CharField(max_length=5, blank=True)
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " (" + self.ip + ") at " + str(self.created_at)


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    method_path = GEOLOCATION_METHOD
    result = None

    if not client_ip:
        client_ip = GEOLOCATION_PLACEHOLDER_IP

    else:
        if not is_routable:
            result = {"error": True, "reason": "Address not routable"}

        elif method_path:
            module_name, func_name = method_path.rsplit('.', 1)
            try:
                module = importlib.import_module(module_name)
                geolocation_func = getattr(module, func_name)
                result = geolocation_func(client_ip)
            except (ImportError, AttributeError) as er:
                raise ValueError("Invalid geolocation method specified in settings.\n", er) from er

    if not result:
        result = get_geolocation_data(client_ip)
        assert isinstance(result, dict)

        mapped_fields = {}

        for key, value in result.items():

            if key in GEOLOCATION_BLOCK_FIELDS:
                continue

            try:
                _ = Login._meta.get_field(key)
                mapped_fields[key] = value
            except FieldDoesNotExist:
                pass

    _ = Login.objects.create(
        user=user,
        ip=client_ip,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        ip_info=result,
        **mapped_fields
    )
