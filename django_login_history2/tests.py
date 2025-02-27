from unittest.mock import patch, MagicMock
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.utils import timezone

from django_login_history2.app_settings import get_geolocation_helper_class
from django_login_history2.helper import IPCheckerTestMode, IPCheckerIPApi
from django_login_history2.models import Login
from django_login_history2.mock.ip_api import (get_mock, RESERVED_IP_ADDRESS_RESPONSE, INVALID_IP_ADDRESS_RESPONSE,
                                               SUCCESS_RESPONSE, QUOTA_EXCEEDED_RESPONSE, INVALID_KEY_RESPONSE)

class LoginHistoryTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

        self.google_request = self.factory.get('/', REMOTE_ADDR='8.8.8.8')
        self.google_request.user = self.user

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

    @patch('django_login_history2.helper.IPCheckerIPApi.api_get')
    def test_not_routable_ip(self, mock_get: MagicMock):
        mock_get.return_value = get_mock(SUCCESS_RESPONSE)
        mock_get.return_value.__enter__.return_value = get_mock(SUCCESS_RESPONSE)

        instance = IPCheckerIPApi(self.request, self.user)
        self.assertFalse(instance.is_routable)
        data = instance.get_geolocation_data()
        mock_get.assert_not_called()
        self.assertTrue(data.error)
        self.assertEqual(data.error_reason, 'Address not routable')

    @patch('django_login_history2.helper.IPCheckerIPApi.api_get')
    def test_routable_ip(self, mock_get: MagicMock):
        mock_get.return_value = get_mock(SUCCESS_RESPONSE)
        mock_get.return_value.__enter__.return_value = get_mock(SUCCESS_RESPONSE)
        instance = IPCheckerIPApi(self.google_request, self.user)
        self.assertTrue(instance.is_routable)
        data = instance.get_geolocation_data()
        mock_get.assert_called_once()
        self.assertFalse(data.error)
        self.assertIn(data.error_reason, (None, ''))

    @patch('django_login_history2.helper.IPCheckerIPApi.api_get')
    def test_ip_api_quota_exceeded(self, mock_get: MagicMock):
        mock_get.return_value = get_mock(QUOTA_EXCEEDED_RESPONSE)
        mock_get.return_value.__enter__.return_value = get_mock(QUOTA_EXCEEDED_RESPONSE)
        instance = IPCheckerIPApi(self.google_request, self.user)
        self.assertTrue(instance.is_routable)
        data = instance.get_geolocation_data()
        mock_get.assert_called_once()
        self.assertTrue(data.error)
        self.assertEqual(data.error_reason, 'RateLimited 127.0.0.1')


    @patch('django_login_history2.helper.IPCheckerIPApi.api_get')
    def test_ip_api_invalid_ip(self, mock_get: MagicMock):
        mock_get.return_value = get_mock(INVALID_IP_ADDRESS_RESPONSE)
        mock_get.return_value.__enter__.return_value = get_mock(INVALID_IP_ADDRESS_RESPONSE)
        instance = IPCheckerIPApi(self.google_request, self.user)
        self.assertTrue(instance.is_routable)
        data = instance.get_geolocation_data()
        mock_get.assert_called_once()
        self.assertTrue(data.error)
        self.assertEqual(data.error_reason, 'Invalid IP Address')


    @patch('django_login_history2.helper.IPCheckerIPApi.api_get')
    def test_ip_api_reserved_ip(self, mock_get: MagicMock):
        mock_get.return_value = get_mock(RESERVED_IP_ADDRESS_RESPONSE)
        mock_get.return_value.__enter__.return_value = get_mock(RESERVED_IP_ADDRESS_RESPONSE)
        instance = IPCheckerIPApi(self.google_request, self.user)
        self.assertTrue(instance.is_routable)
        data = instance.get_geolocation_data()
        mock_get.assert_called_once()
        self.assertTrue(data.error)
        self.assertEqual(data.error_reason, 'Reserved IP Address')


    @patch("django_login_history2.helper.IPCheckerIPApi.api_get")
    def test_ip_api_invalid_key(self, mock_get: MagicMock):
        mock_get.return_value = get_mock(INVALID_KEY_RESPONSE)
        mock_get.return_value.__enter__.return_value = get_mock(INVALID_KEY_RESPONSE)
        instance = IPCheckerIPApi(self.google_request, self.user)
        self.assertTrue(instance.is_routable)
        data = instance.get_geolocation_data()
        mock_get.assert_called_once()
        self.assertTrue(data.error)
        self.assertEqual(data.error_reason, 'Invalid Key Invalid key. SignUp @ https://ipapi.co/pricing/')

