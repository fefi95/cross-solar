from rest_framework.test import APITestCase
from rest_framework import status
from .models import Panel

class PanelTestCase(APITestCase):
    def setUp(self):
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222", latitude=12.345678, longitude=98.7655432)

    def test_panel_listing(self):
        response = self.client.get('/panel/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_panel_get(self):
        response = self.client.get('/panel/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")
