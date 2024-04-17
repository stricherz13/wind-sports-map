from django.urls import path
from . import views

urlpatterns = [
    # other url patterns...
    path('weather/<int:pk>/', views.weather_json, name='weather_view'),
]