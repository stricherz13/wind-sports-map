from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Direction(models.Model):
    direction_choices = (("N", "North"), ("NE", "Northeast"), ("E", "East"), ("SE", "Southeast"), ("S", "South"),
                         ("SW", "Southwest"), ("W", "West"), ("NW", "Northwest"))
    name = models.CharField(max_length=2, choices=direction_choices)

    def __str__(self):
        return self.get_name_display()


class LaunchLocation(models.Model):
    skill_choices = (("Be", "Beginner"), ("In", "Intermediate"), ("Ad", "Advanced"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)
    name = models.CharField(max_length=100, null=False)
    kites = models.BooleanField(default=False, null=False)
    directions = models.ManyToManyField(Direction)
    skill = models.CharField(max_length=15, choices=skill_choices, default="Beginner", null=False)
    parking = models.BooleanField(default=False, null=False)
    public = models.BooleanField(default=False, null=False)
    description = models.TextField()
    # picture = models.ImageField(upload_to='launchlocation', blank=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='launchlocations')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Weather(models.Model):
    id = models.ForeignKey('LaunchLocation', on_delete=models.CASCADE, unique=True, primary_key=True)
    ws_name = models.CharField(max_length=100)
    temp = models.FloatField()
    wind = models.FloatField()
    windgust = models.FloatField(null=True)
    winddirection = models.CharField(max_length=50)
    condition = models.CharField(max_length=20)
    marker = models.CharField(max_length=10, default="red")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


2
