from django.test import TestCase
from django.urls import reverse

from .models import User


class AuthFlowTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@x.com',
            'user_type': 'customer',
            'password1': 'StrongPass#2026',
            'password2': 'StrongPass#2026',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_rejects_mismatched_passwords(self):
        self.client.post(reverse('accounts:signup'), {
            'username': 'baduser',
            'email': 'baduser@x.com',
            'user_type': 'customer',
            'password1': 'StrongPass#2026',
            'password2': 'DifferentPass#2026',
        })
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_login_with_valid_credentials(self):
        User.objects.create_user('member', 'member@x.com', 'pw12345!')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'member',
            'password': 'pw12345!',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_password_shows_error(self):
        User.objects.create_user('member', 'member@x.com', 'pw12345!')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'member',
            'password': 'wrongpassword',
        })
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        User.objects.create_user('member', 'member@x.com', 'pw12345!')
        self.client.login(username='member', password='pw12345!')
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
