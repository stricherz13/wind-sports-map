from rest_framework import generics
from .models import LaunchLocations
from .serializers import LaunchLocationsSerializer


class LaunchLocationsListView(generics.ListAPIView):
    queryset = LaunchLocations.objects.all()
    serializer_class = LaunchLocationsSerializer
