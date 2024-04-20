from rest_framework import serializers
from .models import LaunchLocation, Weather


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class LaunchLocationSerializer(serializers.ModelSerializer):
    weatherstation = WeatherDataSerializer(many=False, read_only=True)

    class Meta:
        model = LaunchLocation
        fields = '__all__'
