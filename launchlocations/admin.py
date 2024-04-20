from django.contrib import admin
from .models import LaunchLocation, Weather, Direction

admin.site.register(LaunchLocation)
admin.site.register(Weather)
admin.site.register(Direction)
