from datetime import datetime, timezone

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
    }
]


def updatemarker(lat, lng, direction):
    currentTimeUTC = datetime.now(timezone.utc)
    formattedCurrentTime = currentTimeUTC.strftime("%I:%M:%S %p")
    try:
        url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&timezone=UTC"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sunrise = data['results']['sunrise']
            sunset = data['results']['sunset']
            print(f"Sunrise: {sunrise} | Sunset: {sunset} | Current Time: {formattedCurrentTime}")
            if sunrise > formattedCurrentTime < sunset:
                try:
                    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=6ece76affa411be60affa4ee66ee2d62&units=imperial"
                    response = requests.get(url)
                    x = response.json()
                    if x["cod"] != "404":
                        name = x["name"]
                        temp = x["main"]["temp"]
                        wind = round(float(x["wind"]["speed"] * 0.869), 2)
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
                        print(
                            f"The {name} weather station is currently reporting a wind speed of {wind} knots. The "
                            f"wind is coming from the {winddirection} direction. The gusts are reaching up to "
                            f"{windgust} knots. The current temperature is {temp} degrees Fahrenheit.")
                        if wind >= 10.00 and winddirection in direction and temp >= 50.00:
                            print("Green")
                        elif wind >= 10.00 and winddirection not in direction and temp >= 30.00:
                            print("Yellow")
                        else:
                            print("Red")
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
        updatemarker(lat, lng, direction)
    time.sleep(3600)  # sleep for 1 hour
