# apps/users/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase  # APITestCase lebih cocok untuk API
from .models import User


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('users_api:register')
        self.login_url = reverse('users_api:login')
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'phone': '1234567890',
            'role': 'user'
        }
        self.user_login_data = {
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!'
        }

    def test_user_registration_success(self):
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])
        self.assertIn('token', response.data)

    def test_user_registration_password_mismatch(self):
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'WrongPassword'
        response = self.client.post(
            self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)

    def test_user_login_success(self):
        # Pertama, daftarkan user
        self.client.post(self.register_url, self.user_data, format='json')
        # Kemudian, coba login
        response = self.client.post(
            self.login_url, self.user_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']
                         ['email'], self.user_data['email'])

    def test_user_login_failure_wrong_password(self):
        self.client.post(self.register_url, self.user_data, format='json')
        wrong_login_data = {
            'email': self.user_data['email'], 'password': 'WrongPassword'}
        response = self.client.post(
            self.login_url, wrong_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    # Tambahkan test untuk profile, change password, logout, permissions, dll.
