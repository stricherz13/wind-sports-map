import os
from datetime import datetime, timedelta
import requests
from .models import LaunchLocation, Weather


def update_weather_data():
    currentTimeUTC = datetime.utcnow()
    launch_locations = LaunchLocation.objects.all()
    for location in launch_locations:
        try:
            url = f"https://api.sunrise-sunset.org/json?lat={location.lat}&lng={location.lng}&formatted=0"
            response = requests.get(url)
            if response.status_code != 200:
                print("Error in request for sunrise-sunset data")
                continue

            data = response.json()
            sunrise_str = data["results"]["sunrise"]
            sunset_str = data["results"]["sunset"]
            sunrise = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M:%S+00:00")
            sunset = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M:%S+00:00")

            if currentTimeUTC < sunrise:
                sunrise -= timedelta(days=1)
                sunset -= timedelta(days=1)

            if sunrise < currentTimeUTC < sunset:
                try:
                    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.lat}&lon={location.lng}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=imperial"
                    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.lat}&lon={location.lng}&appid=6ece76affa411be60affa4ee66ee2d62&units=imperial"
                    print(f"Sending request to: {url}")
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
                        winddirection = get_wind_direction(degrees)

                        if (12.00 <= wind < 33.00 and winddirection in location.direction and temp >= 50.00 and
                                condition not in ["Rain", "Snow", "Thunderstorm"]):
                            marker = "Green"
                        elif 10.00 <= wind < 40.00 and temp >= 30.00:
                            marker = "Yellow"
                        else:
                            marker = "Red"

                        weather, created = Weather.objects.update_or_create(
                            launch_id=location,
                            defaults={
                                'ws_name': ws_name,
                                'temp': temp,
                                'wind': wind,
                                'windgust': windgust,
                                'winddirection': winddirection,
                                'condition': condition,
                                'marker': marker
                            }
                        )
                except requests.ConnectionError:
                    print("No Internet Connection")
                    continue
            else:
                marker = "Gray"
                weather, created = Weather.objects.update_or_create(
                    launch_id=location,
                    defaults={
                        'ws_name': None,
                        'temp': None,
                        'wind': None,
                        'windgust': None,
                        'winddirection': None,
                        'condition': None,
                        'marker': marker
                    }
                )
                if not created:
                    weather.save(update_fields=['marker'])
        except Exception as e:
            print(f"Error in request: {e}")
            continue


def get_wind_direction(degrees):
    if degrees >= 348.75 or degrees <= 33.74:
        return "North"
    elif 33.75 <= degrees <= 78.74:
        return "Northeast"
    elif 75.75 <= degrees <= 123.74:
        return "East"
    elif 123.75 <= degrees <= 168.74:
        return "Southeast"
    elif 168.75 <= degrees <= 213.74:
        return "South"
    elif 213.75 <= degrees <= 258.74:
        return "Southwest"
    elif 258.75 <= degrees <= 303.74:
        return "West"
    elif 303.75 <= degrees <= 348.74:
        return "Northwest"
