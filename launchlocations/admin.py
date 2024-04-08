from django.contrib import admin
from .models import LaunchLocations, Weather

admin.site.register(LaunchLocations)
admin.site.register(Weather)
