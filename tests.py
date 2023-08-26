from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.test import TestCase
from django.dispatch import receiver
from django_login_history2.models import Login, post_login


class LoginHistoryTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_user_logged_in(self):

        @receiver(user_logged_in)
        def user_logged_in_callback(sender, request, user, **kwargs):
            post_login(sender=sender, request=request, user=user, **kwargs)

        self.client.login(username='testuser', password='testpass')
        self.client.logout()
        self.assertTrue(Login.objects.count() > 0)
