from django.test import TestCase
from .models import LaunchLocation, Weather, Direction
from .serializers import LaunchLocationSerializer, WeatherDataSerializer
from django.contrib.auth.models import User


class LaunchLocationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.direction = Direction.objects.create(name='N')
        self.launch_location = LaunchLocation.objects.create(
            lat=1.0, lng=1.0, name='Test Location', kites=True,
            skill='Be', parking=True, public=True, description='Test Description',
            user=self.user
        )
        self.launch_location.direction.add(self.direction)

    def test_launch_location_creation(self):
        self.assertEqual(LaunchLocation.objects.count(), 1)


class WeatherModelTest(TestCase):
    def setUp(self):
        self.weather = Weather.objects.create(
            ws_name='Test Weather', temp=20.0, wind=5.0, windgust=10.0,
            winddirection='N', condition='Clear', marker='red'
        )

    def test_weather_creation(self):
        self.assertEqual(Weather.objects.count(), 1)


class DirectionModelTest(TestCase):
    def setUp(self):
        self.direction = Direction.objects.create(name='N')

    def test_direction_creation(self):
        self.assertEqual(Direction.objects.count(), 1)


class LaunchLocationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.direction = Direction.objects.create(name='N')
        self.launch_location = LaunchLocation.objects.create(
            lat=1.0, lng=1.0, name='Test Location', kites=True,
            skill='Be', parking=True, public=True, description='Test Description',
            user=self.user
        )
        self.launch_location.direction.add(self.direction)
        self.serializer = LaunchLocationSerializer(instance=self.launch_location)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['id', 'lat', 'lng', 'name', 'kites', 'direction', 'skill', 'parking', 'public',
                               'description', 'weatherstation', 'user', 'updated_at'])


class WeatherDataSerializerTest(TestCase):
    def setUp(self):
        self.weather = Weather.objects.create(
            ws_name='Test Weather', temp=20.0, wind=5.0, windgust=10.0,
            winddirection='N', condition='Clear', marker='red'
        )
        self.serializer = WeatherDataSerializer(instance=self.weather)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['id', 'launch_id', 'ws_name', 'temp', 'wind', 'windgust', 'winddirection', 'condition',
                               'marker', 'updated_at'])
