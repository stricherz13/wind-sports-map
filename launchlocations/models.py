from django.db import models
from django.contrib.auth.models import User
import uuid


class Direction(models.Model):
    direction_choices = [("N", "North"), ("NE", "Northeast"), ("E", "East"), ("SE", "Southeast"), ("S", "South"),
                         ("SW", "Southwest"), ("W", "West"), ("NW", "Northwest")]
    name = models.CharField(max_length=2, choices=direction_choices)

    def __str__(self):
        return self.name


class LaunchLocation(models.Model):
    skill_choices = (("Be", "Beginner"), ("In", "Intermediate"), ("Ad", "Advanced"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)
    name = models.CharField(max_length=100, null=False)
    kites = models.BooleanField(default=False, null=False)
    direction = models.ManyToManyField(Direction, blank=False)
    skill = models.CharField(max_length=15, choices=skill_choices, default="Beginner", null=False)
    parking = models.BooleanField(default=False, null=False)
    public = models.BooleanField(default=False, null=False)
    description = models.TextField()
    weatherstation = models.ForeignKey('Weather', null=True, on_delete=models.SET_NULL, related_name='launchlocations')
    # picture = models.ImageField(upload_to='launchlocation', blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='users')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Weather(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    launch_id = models.ForeignKey('LaunchLocation', on_delete=models.CASCADE, null=True)
    ws_name = models.CharField(max_length=100, null=True)
    temp = models.FloatField(null=True)
    wind = models.FloatField(null=True)
    windgust = models.FloatField(null=True)
    winddirection = models.CharField(max_length=50, null=True)
    condition = models.CharField(max_length=20, null=True)
    marker = models.CharField(max_length=10, default="red")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ws_name)


2
