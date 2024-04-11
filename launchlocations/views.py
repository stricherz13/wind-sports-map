from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Weather, LaunchLocation
from .serializers import WeatherDataSerializer
import requests
from datetime import datetime


class UpdateMarkerView(APIView):
    def get(self, request, *args, **kwargs):
        launch_location_id = self.kwargs.get('id')
        launch_location = get_object_or_404(LaunchLocation, id=launch_location_id)

        lat = launch_location.lat
        lng = launch_location.lng
        direction = launch_location.directions.all()
        name = launch_location.name

        current_time_utc = datetime.utcnow()
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sunrise_str = data["results"]["sunrise"]
            sunset_str = data["results"]["sunset"]
            sunrise = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M:%S+00:00")
            sunset = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M:%S+00:00")
            if sunrise < current_time_utc < sunset:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=6ece76affa411be60affa4ee66ee2d62&units=imperial"
                response = requests.get(url)
                x = response.json()
                if x["cod"] != "404":
                    ws_name = x["name"]
                    temp = x["main"]["temp"]
                    wind = round(float(x["wind"]["speed"] * 0.869), 2)
                    condition = x["weather"][0]["main"]
                    try:
                        windgust = round(float(x["wind"]["gust"] * 0.869), 2)
                    except KeyError:
                        windgust = None
                    degrees = float(x["wind"]["deg"])
                    if degrees >= 348.75 or degrees <= 33.74:
                        winddirection = "North"
                    elif 33.75 <= degrees <= 78.74:
                        winddirection = "Northeast"
                    elif 75.75 <= degrees <= 123.74:
                        winddirection = "East"
                    elif 123.75 <= degrees <= 168.74:
                        winddirection = "Southeast"
                    elif 168.75 <= degrees <= 213.74:
                        winddirection = "South"
                    elif 213.75 <= degrees <= 258.74:
                        winddirection = "Southwest"
                    elif 258.75 <= degrees <= 303.74:
                        winddirection = "West"
                    elif 303.75 <= degrees <= 348.74:
                        winddirection = "Northwest"
                    if 10.00 <= wind < 33.00 and winddirection in direction and temp >= 50.00 and condition not in [
                        "Rain", "Snow", "Thunderstorm"]:
                        marker = "Green"
                    elif 10.00 <= wind < 40.00 and temp >= 30.00:
                        marker = "Yellow"
                    else:
                        marker = "Red"
                    weather_data = {
                        "ws_name": ws_name,
                        "temp": temp,
                        "wind": wind,
                        "windgust": windgust,
                        "winddirection": winddirection,
                        "condition": condition,
                        "marker": marker
                    }
                else:
                    weather_data = {"error": "Error in request"}
            else:
                weather_data = {"marker": "Gray"}
        else:
            weather_data = {"error": "Error in request"}

            weather_data_instance = Weather.objects.create(**weather_data)
            serializer = WeatherDataSerializer(weather_data_instance)

            return Response(serializer.data)
