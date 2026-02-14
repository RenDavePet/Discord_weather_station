#!/usr/bin/env python3
"""
Discord Weather Bot - Sends daily weather updates at 9 AM
Uses Open-Meteo API for weather data and Discord API for messaging
"""

from weather import WeatherFetcher
from discord_bot import DiscordBot

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def send_weather_to_discord():
    """Fetch weather and send to Discord channel"""
    print("=" * 60)
    print("Fetching weather data...")
    
    # Fetch weather
    weather_fetcher = WeatherFetcher()
    weather_data = weather_fetcher.fetch_weather()
    
    if not weather_data:
        print("❌ Failed to fetch weather data")
        return False
    
    # Format weather message
    weather_message = weather_fetcher.format_weather_message(weather_data)
    print("\nWeather data retrieved successfully!")
    print(weather_message)
    
    # Send to Discord
    print("\n" + "=" * 60)
    print("Sending to Discord...")
    
    try:
        bot = DiscordBot()
        result = bot.send_weather_update(weather_message, use_embed=True)
        
        if result:
            print("✅ Weather update sent to Discord successfully!")
            return True
        else:
            print("❌ Failed to send weather update to Discord")
            return False
    except ValueError as e:
        print(f"❌ Discord bot configuration error: {e}")
        print("\n📝 Please update your .env file with:")
        print("   - DISCORD_BOT_TOKEN=your_bot_token_here")
        print("   - DISCORD_CHANNEL_ID=your_channel_id_here")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    print("🤖 Discord Weather Bot - Manual Test")
    print("=" * 60)
    send_weather_to_discord()
    print("=" * 60)

