from rest_framework import serializers
from .models import LaunchLocation, Weather


class LaunchLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchLocation
        fields = '__all__'


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'
