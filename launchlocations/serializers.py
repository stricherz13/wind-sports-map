from rest_framework import serializers
from .models import LaunchLocation


class LaunchLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchLocation
        fields = '__all__'
