import requests


LOCATION = "București"

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):
    params = {"name": city, "count": 1, "language": "ro", "format": "json"}
    resp = requests.get(GEOCODING_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("results"):
        print(f"Locația '{city}' nu a fost găsită.")
        return None
    result = data["results"][0]
    return result["latitude"], result["longitude"], result.get("name", city)


def get_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "auto",
    }
    resp = requests.get(WEATHER_URL, params=params)
    resp.raise_for_status()
    return resp.json()


def main():
    coords = get_coordinates(LOCATION)
    if coords is None:
        return
    lat, lon, name = coords
    print(f"Locație: {name}")
    print(f"Coordonate: {lat:.4f}, {lon:.4f}")
    print("-" * 30)

    weather = get_weather(lat, lon)
    current = weather["current_weather"]
    temp = current["temperature"]
    wind = current["windspeed"]
    unit_temp = weather["current_weather_units"]["temperature"]
    unit_wind = weather["current_weather_units"]["windspeed"]

    print(f"Temperatură: {temp}{unit_temp}")
    print(f"Viteza vântului: {wind}{unit_wind}")


if __name__ == "__main__":
    main()
