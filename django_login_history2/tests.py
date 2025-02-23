from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.utils import timezone

from django_login_history2.app_settings import get_geolocation_helper_class
from django_login_history2.helper import IPCheckerTestMode
from django_login_history2.models import Login


class LoginHistoryTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_class_helper(self):
        self.assertEqual(get_geolocation_helper_class(), IPCheckerTestMode)
        obj = get_geolocation_helper_class()(self.request, self.user)
        self.assertEqual(obj.user, self.request.user)
        self.assertEqual(obj.client_ip, '127.0.0.1')

    def test_user_login_logout(self):
        self.client.login(username='testuser', password='testpass')
        self.assertTrue(Login.objects.count() > 0)

        obj = self.user.login_history.last()
        str_login = str(obj)
        login_ts = timezone.now() - obj.login_at

        self.assertTrue(login_ts <= timedelta(seconds=5))
        self.client.logout()

        obj.refresh_from_db()
        str_logout = str(obj)

        self.assertNotEqual(str_login, str_logout)
        logout_ts = timezone.now() - obj.logout_at
        self.assertTrue(logout_ts <= timedelta(seconds=5))