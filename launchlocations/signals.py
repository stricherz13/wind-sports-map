import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LaunchLocation, Weather


@receiver(post_save, sender=LaunchLocation)
def create_weatherstation(sender, instance, created, **kwargs):
    if created:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={instance.lat}&lon={instance.lng}&appid=6ece76affa411be60affa4ee66ee2d62&units=imperial"
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

                location_direction = directionList(instance)

                if (12.00 <= wind < 33.00 and winddirection in location_direction and temp >= 50.00 and
                        condition not in ["Rain", "Snow", "Thunderstorm"]):
                    marker = "Green"
                elif 10.00 <= wind < 40.00 and temp >= 30.00:
                    marker = "Yellow"
                else:
                    marker = "Red"

                weather = Weather.objects.create(
                    launch_id=instance,
                    ws_name=ws_name,
                    temp=temp,
                    wind=wind,
                    windgust=windgust,
                    winddirection=winddirection,
                    condition=condition,
                    marker=marker
                )
        except requests.ConnectionError:
            print("No Internet Connection")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e


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


def directionList(instance):
    location_direction = []
    for direction in instance.direction.all():
        location_direction.append(direction.name)
    return location_direction
