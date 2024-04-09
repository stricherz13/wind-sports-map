from rest_framework import generics
from .models import LaunchLocation
from .serializers import LaunchLocationSerializer


class LaunchLocationListView(generics.ListAPIView):
    queryset = LaunchLocation.objects.all()
    serializer_class = LaunchLocationSerializer
