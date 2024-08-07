import requests
import json
from decouple import config

WEATHER_API_KEY = config('WEATHER')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

class City:
    def __init__(self, name, lon, lat):
        self.name = name  # name of the city
        self.lon = lon  # longitude
        self.lat = lat  # latitude

# Example city instance
agadir = City("Agadir", "-9.598107", "30.427755")

def construct_url(city, api_key):
    return (f"{BASE_URL}lat={city.lat}&lon={city.lon}"
            f"&lang=en&units=metric&appid={api_key}")

URL = construct_url(agadir, WEATHER_API_KEY)

def getCurrentWeather():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        data = response.json()

        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]

        temperature = main.get('temp', 'N/A')
        humidity = main.get('humidity', 'N/A')
        pressure = main.get('pressure', 'N/A')
        description = weather.get('description', 'N/A')

        return (f"\n{agadir.name:-^30}\n"
                f"Temperature: {temperature} °C\n"
                f"Humidity: {humidity} %\n"
                f"Pressure: {pressure} hPa\n"
                f"Weather Report: {description}\n")

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        return "Failed to get weather data."

# Example usage
if __name__ == "__main__":
    print(getCurrentWeather())
