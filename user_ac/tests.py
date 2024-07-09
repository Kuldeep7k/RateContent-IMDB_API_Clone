from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "example",
            "email": "example@test.com",
            "password": "Example@123",
            "password2": "Example@123"
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Example@123")

    def test_login(self):
        data = {
            "username": "example",
            "password": "Example@123"
        }
        url = reverse('login') 
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
     
        self.token = Token.objects.get(user__username="example")

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('logout')  
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
