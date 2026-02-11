import requests
import os
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WeatherFetcher:
    """Fetches weather data from Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, latitude: float = None, longitude: float = None):
        """
        Initialize WeatherFetcher with coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        """
        self.latitude = latitude
        self.longitude = longitude
    
    def fetch_weather(self) -> Optional[Dict]:
        """
        Fetch current weather and forecast data
        
        Returns:
            Dictionary containing weather data or None if request fails
        """
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "timezone": "auto",
            "forecast_days": 3
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("Error: Request to Open-Meteo API timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_weather_description(self, weather_code: int) -> tuple[str, str]:
        """
        Convert WMO weather code to description and emoji
        
        Args:
            weather_code: WMO weather code
            
        Returns:
            Tuple of (description, emoji)
        """
        weather_codes = {
            0: ("Clear sky", "☀️"),
            1: ("Mainly clear", "🌤️"),
            2: ("Partly cloudy", "⛅"),
            3: ("Overcast", "☁️"),
            45: ("Foggy", "🌫️"),
            48: ("Depositing rime fog", "🌫️"),
            51: ("Light drizzle", "🌦️"),
            53: ("Moderate drizzle", "🌦️"),
            55: ("Dense drizzle", "🌧️"),
            61: ("Slight rain", "🌧️"),
            63: ("Moderate rain", "🌧️"),
            65: ("Heavy rain", "🌧️"),
            71: ("Slight snow", "🌨️"),
            73: ("Moderate snow", "🌨️"),
            75: ("Heavy snow", "❄️"),
            77: ("Snow grains", "🌨️"),
            80: ("Slight rain showers", "🌦️"),
            81: ("Moderate rain showers", "🌧️"),
            82: ("Violent rain showers", "⛈️"),
            85: ("Slight snow showers", "🌨️"),
            86: ("Heavy snow showers", "❄️"),
            95: ("Thunderstorm", "⛈️"),
            96: ("Thunderstorm with slight hail", "⛈️"),
            99: ("Thunderstorm with heavy hail", "⛈️"),
        }
        return weather_codes.get(weather_code, ("Unknown", "🌡️"))
    
    def format_weather_message(self, weather_data: Dict) -> str:
        """
        Format weather data into a readable message
        
        Args:
            weather_data: Weather data from API
            
        Returns:
            Formatted weather message string
        """
        if not weather_data:
            return "❌ Unable to fetch weather data"
        
        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})
        
        # Current weather
        temp = current.get("temperature_2m", "N/A")
        feels_like = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        precipitation = current.get("precipitation", "N/A")
        weather_code = current.get("weather_code", 0)
        
        description, emoji = self.get_weather_description(weather_code)
        
        # Today's forecast
        today_max = daily.get("temperature_2m_max", [None])[0]
        today_min = daily.get("temperature_2m_min", [None])[0]
        today_precip = daily.get("precipitation_sum", [None])[0]
        
        message = f"""🌤️ **Weather Report** 🌤️
📍 Location: {self.latitude}, {self.longitude}
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Current Conditions** {emoji}
{description}
🌡️ Temperature: {temp}°C (feels like {feels_like}°C)
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} km/h
🌧️ Precipitation: {precipitation} mm

**Today's Forecast**
📈 High: {today_max}°C
📉 Low: {today_min}°C
☔ Precipitation: {today_precip} mm
"""
        return message


if __name__ == "__main__":
    # Test the weather fetcher
    LATITUDE = float(os.getenv("LATITUDE"))
    LONGITUDE = float(os.getenv("LONGITUDE"))
    if not LATITUDE or not LONGITUDE:
        raise ValueError("Latitude and longitude not set in environment variables")

    fetcher = WeatherFetcher(LATITUDE, LONGITUDE)
    print("Fetching weather data...")
    data = fetcher.fetch_weather()
    
    if data:
        print("\n" + "="*50)
        print(fetcher.format_weather_message(data))
        print("="*50)
    else:
        print("Failed to fetch weather data")
