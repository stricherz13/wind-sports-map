import requests
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Weather(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    launch_id = models.ForeignKey("LaunchLocation", on_delete=models.CASCADE, null=True)
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


class Direction(models.Model):
    direction_choices = [
        ("N", "North"),
        ("NE", "Northeast"),
        ("E", "East"),
        ("SE", "Southeast"),
        ("S", "South"),
        ("SW", "Southwest"),
        ("W", "West"),
        ("NW", "Northwest"),
    ]
    name = models.CharField(max_length=2, choices=direction_choices)

    def __str__(self):
        return self.name


class LaunchLocation(models.Model):
    skill_choices = (("Be", "Beginner"), ("In", "Intermediate"), ("Ad", "Advanced"))
    STATUS_CHOICES = [
        ("DR", "Draft"),
        ("AP", "Approved"),
        ("PU", "Published"),
        ("RE", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.FloatField(
        null=False, validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    lng = models.FloatField(
        null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    name = models.CharField(max_length=100, null=False)
    kites = models.BooleanField(default=False, null=False)
    direction = models.ManyToManyField(Direction, blank=False)
    skill = models.CharField(
        max_length=15, choices=skill_choices, default="Beginner", null=False
    )
    parking = models.BooleanField(default=False, null=False)
    public = models.BooleanField(default=False, null=False)
    description = models.TextField()
    weatherstation = models.OneToOneField(Weather, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="DR")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return str(self.name)
