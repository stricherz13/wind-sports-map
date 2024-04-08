from django.db import models
import uuid


class Direction(models.Model):
    direction_choices = (("N", "North"), ("NE", "Northeast"), ("E", "East"), ("SE", "Southeast"), ("S", "South"),
                         ("SW", "Southwest"), ("W", "West"), ("NW", "Northwest"))
    name = models.CharField(max_length=2, choices=direction_choices)

    def __str__(self):
        return self.get_name_display()


class LaunchLocations(models.Model):
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
    # picture = models.ImageField(upload_to='launchlocations', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Weather(models.Model):
    id = models.ForeignKey('LaunchLocations', on_delete=models.CASCADE, unique=True, primary_key=True)
    ws_name = models.CharField(max_length=100)
    temp = models.FloatField()
    wind = models.FloatField()
    windgust = models.FloatField()
    winddirection = models.CharField(max_length=100)
    marker = models.CharField(max_length=10, default="red")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


2
