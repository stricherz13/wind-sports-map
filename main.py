from datetime import datetime, timedelta

import requests
import time

launchsites = [
    {
        "Name": "Heldmann Picnic Shelter",
        "lat": 38.721046505414385,
        "lng": -90.47979591356747,
        "direction": ["West", "Northwest", "North", "Northeast", "East", "Southwest"]
    },
    {
        "Name": "Soccer Field",
        "lat": 38.716795409273914,
        "lng": -90.48780038642688,
        "direction": ["North", "Northeast", "East", "Southeast", "South"]
    },
    {
        "Name": "Space Balls",
        "lat": 38.63217901420372,
        "lng": -89.28922801088844,
        "direction": ["North", "Northeast", "East", "West", "Northwest"]
    },
    {
        "Name": "Rend Lake (North Marcum)",
        "lat": 38.05135955074948,
        "lng": -88.95676326852967,
        "direction": ["North", "Northeast", "South", "Southwest", "West", "Northwest"]
    },
    {
        "Name": "South Haven",
        "lat": 42.402870500131954,
        "lng": -86.28366931556243,
        "direction": ["Southwest", "West", "Northwest", "North"]
    },
    {
        "Name": "Lake Poinsett",
        "lat": 44.53875172083404,
        "lng": -97.07681880361784,
        "direction": ["Northeast", "West", "Northwest", "North"]
    },
    {
        "Name": "Stockton Lake (West Launch)",
        "lat": 37.67556554494834,
        "lng": -93.7718652208572,
        "direction": ["South", "Southeast", "East", "Northeast", "North", "Northwest"]
    },
    {
        "Name": "Silver Creek (Sunset Bay Beach Park",
        "lat": 42.564415590075406,
        "lng": -79.13901397057322,
        "direction": ["North", "Southwest", "West", "Northwest"]
    }
]


def updatemarker(lat, lng, direction, name):
    currentTimeUTC = datetime.utcnow()
    try:
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sunrise_str = data["results"]["sunrise"]
            sunset_str = data["results"]["sunset"]
            sunrise = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M:%S+00:00")
            sunset = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M:%S+00:00")
            # print(f"Sunrise: {sunrise} | Sunset: {sunset} | Current Time: {currentTimeUTC}")
            if currentTimeUTC < sunrise:
                sunrise -= timedelta(days=1)
                sunset -= timedelta(days=1)
            if sunrise < currentTimeUTC < sunset:
                try:
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
                        if 12.00 <= wind < 33.00 and winddirection in direction and temp >= 50.00 and condition not in [
                            "Rain", "Snow", "Thunderstorm"]:
                            print("Green: Optimal Conditions")
                            if windgust is None:
                                print(
                                    f"At {name}, {ws_name} weather station is currently reporting a wind speed of {wind}"
                                    f" knots. The wind is coming from the {winddirection} direction. The current "
                                    f"temperature is {temp} degrees Fahrenheit.")
                            else:
                                print(
                                    f"At {name}, {ws_name} weather station is currently reporting a wind speed of {wind} knots. The"
                                    f" wind is coming from the {winddirection} direction. The gusts are reaching up to "
                                    f"{windgust} knots. The current temperature is {temp} degrees Fahrenheit.")
                        elif 10.00 <= wind < 40.00 and temp >= 30.00:
                            print("Yellow: Suboptimal Conditions")
                            if windgust is None:
                                print(
                                    f"At {name}, {ws_name} weather station is currently reporting a wind speed of {wind}"
                                    f" knots. The wind is coming from the {winddirection} direction. The current "
                                    f"temperature is {temp} degrees Fahrenheit.")
                            else:
                                print(
                                    f"At {name}, {ws_name} weather station is currently reporting a wind speed of {wind} knots. The "
                                    f" wind is coming from the {winddirection} direction. The gusts are reaching up to "
                                    f"{windgust} knots. The current temperature is {temp} degrees Fahrenheit.")
                        else:
                            print("Red: Poor Conditions")
                except requests.ConnectionError:
                    return "No Internet Connection"
            else:
                print("Marker Grayed out")
        else:
            print("Error in request 2")
            return
    except:
        print("Error in request 1")
        return


while True:
    for launchsite in launchsites:
        lat = launchsite["lat"]
        lng = launchsite["lng"]
        direction = launchsite["direction"]
        name = launchsite["Name"]
        updatemarker(lat, lng, direction, name)
    time.sleep(360)  # sleep for 1 hour = 3600 seconds
