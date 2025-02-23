import importlib
from dataclasses import asdict
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.exceptions import FieldDoesNotExist
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from .dto import IPInfo
from .app_settings import (GEOLOCATION_METHOD, GEOLOCATION_BLOCK_FIELDS)


class LoginQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        if "login_at" in kwargs:
            kwargs["created_at"] = kwargs.pop("login_at")
        return super().filter(*args, **kwargs)

    def order_by(self, *fields):
        new_fields = [field if field != "login_at" else "created_at" for field in fields]
        return super().order_by(*new_fields)


class LoginManager(models.Manager):
    def get_queryset(self):
        return LoginQuerySet(self.model, using=self._db)


class Login(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             db_index=True,
                             verbose_name=_("user"),
                             related_name='login_history')
    ip = models.GenericIPAddressField(db_index=True, verbose_name=_("ip address"))
    ip_info = models.JSONField(default=dict, verbose_name=_("ip info"))
    city = models.CharField(max_length=80, blank=True, verbose_name=_("city"))
    region = models.CharField(max_length=80, blank=True, verbose_name=_("region"))
    region_code = models.CharField(max_length=10, blank=True, verbose_name=_("region code"))
    country_code = models.CharField(max_length=2, blank=True, verbose_name=_("country code"))
    country_name = models.CharField(max_length=80, blank=True, verbose_name=_("country name"))
    currency = models.CharField(max_length=5, blank=True, verbose_name=_("currency"))
    user_agent = models.TextField(verbose_name=_("user agent"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"), db_index=True)
    logout_at = models.DateTimeField(null=True, blank=True, verbose_name=_("logout at"), db_index=True)
    objects = LoginManager()

    @property
    def login_at(self):
        return self.created_at

    def __str__(self):
        user = getattr(self.user, "username", self.ip)
        logout = ''

        if self.logout_at:
            logout = f' and logout at {self.logout_at}'

        return f"{user} logged in at {self.created_at}{logout}"


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    method_path = GEOLOCATION_METHOD
    result = None
    module_name, func_name = method_path.rsplit('.', 1)

    try:
        module = importlib.import_module(module_name)
        geolocation_func = getattr(module, func_name)
        result = geolocation_func(request, user)
    except (ImportError, AttributeError) as er:
        raise ValueError("Invalid geolocation method specified in settings.\n", er) from er

    if result:
        assert isinstance(result, IPInfo)
        mapped_fields = {}
        result_dict = asdict(result)

        for key, value in result_dict.items():
            if key in GEOLOCATION_BLOCK_FIELDS:
                continue

            try:
                _ = Login._meta.get_field(key)
                mapped_fields[key] = value
            except FieldDoesNotExist:
                pass

        _ = Login.objects.create(
            user=user,
            ip=result.ip,
            user_agent=result.user_agent,
            ip_info=result_dict,
            **mapped_fields
        )


@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    last_login = Login.objects.filter(user=user).latest("created_at")
    last_login.logout_at = timezone.now()
    last_login.save(update_fields=["logout_at"])
