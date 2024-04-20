from rest_framework import generics
from .models import Weather, LaunchLocation
from .serializers import WeatherDataSerializer, LaunchLocationSerializer


class LaunchLocationListView(generics.ListCreateAPIView):
    queryset = LaunchLocation.objects.all()
    serializer_class = LaunchLocationSerializer


class LaunchLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LaunchLocation.objects.all()
    serializer_class = LaunchLocationSerializer


class WeatherDataListView(generics.ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherDataSerializer

class WeatherDataDetailView(generics.ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherDataSerializer