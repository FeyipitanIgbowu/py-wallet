from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.data = {
            "first_name": "Feyi",
            "last_name": "igbowu",
            "email": "feyiigbowu@gmail.com",
            "phone_number": "090887766",
            "username": "fayyyy",
            "password": "123rre"
        }

    def test_signup_returns_201(self):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_returns_400(self):
        data = {
            "first_name": "Feyi",
            "last_name": "igbowu",
            "email": "feyiigbowugmail",
            "phone_number": "090887766",
            "username": "fayyyy",
            "password": "123rre"
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_login_returns_201(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('login')
        login_response = self.client.post(url, self.data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_that_login_fails_with_invalid_credentials(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_data = {
            "email": "feyiigbowu@gmail.com",
            "password": "123rr"
        }
        login_response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)

