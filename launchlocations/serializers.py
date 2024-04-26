from rest_framework import serializers
from .models import LaunchLocation, Weather


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class LaunchLocationSerializer(serializers.ModelSerializer):
    weatherstation = WeatherDataSerializer(many=False, read_only=True)
    user = serializers.StringRelatedField()
    direction = serializers.StringRelatedField(many=True)

    class Meta:
        model = LaunchLocation
        fields = '__all__'
