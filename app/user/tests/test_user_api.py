from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Helper function to create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating new user with a valid payload is successful"""
        payload = {
            'email': 'smirnovserg.s@gmail.com',
            'password': '123456',
            'name': 'serg',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)

        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        """Test creating a new user that already exists fails"""
        payload = {
            'email': 'smirnovserg.s@gmail.com',
            'password': '123456',
            'name': 'Test',
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be not shorter than 5 chars"""
        payload = {
            'email': 'smirnovserg.s@gmail.com',
            'password': '12',
            'name': 'Test',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
