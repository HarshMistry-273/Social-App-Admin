from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class TestUrls(APITestCase):
    def test_endpoint(self):
        url = reverse('root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)