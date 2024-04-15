from django.test import TestCase, Client
from django.urls import reverse
from .models import Weather, LaunchLocation, Direction
import unittest
from unittest.mock import patch
from launchlocations import weather_update


class UpdateMarkerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        directions = ["N", "NE", "E", "W", "NW"]
        direction_instances = [Direction.objects.create(name=direction) for direction in directions]  # create Direction instances
        self.launch_location = LaunchLocation.objects.create(
            name="Space Balls",
            lat=38.63217901420372,
            lng=-89.28922801088844,
        )
        self.launch_location.directions.set(direction_instances)

        self.url = reverse('update_marker', kwargs={'id': self.launch_location.id})

    def test_update_marker(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Weather.objects.filter(ws_name=self.launch_location.name).exists())


class WeatherUpdateTestCase(unittest.TestCase):
    @patch('weather_update.requests.get')
    def test_update_weather_data_success(self, mock_get):
        # Mock response from the OpenWeather API
        mock_response = {
            'wind': {'speed': 5.0}  # Example wind speed data
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Call the function being tested
        weather_update()

        # Assert that the database is updated correctly
        # Add your assertions here

    @patch('your_app.weather_update.requests.get')
    def test_update_weather_data_failure(self, mock_get):
        # Mock a failed response from the OpenWeather API
        mock_get.return_value.status_code = 404

        # Call the function being tested
        weather_update()

        # Assert that the database is not updated in case of failure
        # Add your assertions here

if __name__ == '__main__':
    unittest.main()

