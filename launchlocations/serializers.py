from rest_framework import serializers
from .models import LaunchLocations


class LaunchLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchLocations
        fields = '__all__'
