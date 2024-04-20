from django.urls import path, include
from .views import LaunchLocationListView, LaunchLocationDetailView, WeatherDataListView, WeatherDataDetailView

urlpatterns = [
    path('LaunchLocations/', LaunchLocationListView.as_view()),
    path('LaunchLocations/<uuid:pk>/', LaunchLocationDetailView.as_view()),
    path('WeatherStations/', WeatherDataListView.as_view()),
    path('WeatherStations/<int:pk>/', WeatherDataDetailView.as_view()),
]
