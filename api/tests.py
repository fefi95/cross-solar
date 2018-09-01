from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.management import call_command
from .models import Panel

class PanelTestCase(APITestCase):
    def setUp(self):
        # I decided to use a fixture to make the tests code more readable 
        # and the fixtures file can be modificated to add any data you want
        call_command("loaddata", "cross_solar/fixtures/db.json")

    def check_day_stats(self, data, date, sum, avg, min, max):
        self.assertEqual(data['datetime'].date(), date.date())
        self.assertEqual(data['sum'], sum)
        self.assertEqual(round(data['average'], 3), avg)
        self.assertEqual(data['maximum'], min)
        self.assertEqual(data['minimum'], max)

    def test_panel_listing(self):
        response = self.client.get('/api/panel/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_panel_get(self):
        response = self.client.get('/api/panel/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")

    def test_dayly_stats_panel_2_empty(self):
        response = self.client.get('/api/panel/2/analytics/day/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_dayly_stats_panel_1(self):
        response = self.client.get('/api/panel/1/analytics/day/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.check_day_stats(
            response.data[0], datetime(2018, 8, 20), 5200, 2600.0, 5000, 200
        )
        self.check_day_stats(
            response.data[1], datetime(2018, 8, 30), 4100, 1366.667, 2000, 100
        )
    # Note: There is no need for more tests regarding the stats because django
    # had already tested their functionalitys for calculating everything.

    def test_dayly_stats_panel_not_exists(self):
        response = self.client.get('/api/panel/4/analytics/day/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
