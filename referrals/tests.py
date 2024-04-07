from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User
from .serializers import UserSerializer, ReferralSerializer
import uuid


class UserRegistrationAPIViewTestCase(APITestCase):

    def test_user_registration_success(self):
        url = reverse('user-registration')
        data = {'name': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("Test case 1 passed: User creation and attributes verification.")

    def test_user_registration_failure_existing_email(self):
        url = reverse('user-registration')
        data = {'name': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This field is required.')
        print("Test case 2 passed: User creation and attributes verification.")




class UserDetailsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', password='testpassword', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_get_user_details(self):
        url = reverse('user-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user.name)
        print("Test case 1 passed: Get User Details")


class ReferralsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', password='testpassword', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        self.referral_user = User.objects.create_user(name='referraluser', password='referalpassword', referral_code=self.user.id, email='referal@example.com')

    def test_get_referrals(self):
        url = reverse('referrals-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        print("Test case 1 passed: Get Referal api")

