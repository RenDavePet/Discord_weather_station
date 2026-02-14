import requests
import os
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DiscordBot:
    """Discord bot using raw Discord API (no wrappers)"""
    
    BASE_URL = "https://discord.com/api/v10"
    
    def __init__(self, bot_token: str = None, channel_id: str = None):
        """
        Initialize Discord bot
        
        Args:
            bot_token: Discord bot token (defaults to .env value)
            channel_id: Channel ID to send messages to (defaults to .env value)
        """
        self.bot_token = bot_token or os.getenv("DISCORD_BOT_TOKEN")
        self.channel_id = channel_id or os.getenv("DISCORD_CHANNEL_ID")
        
        if not self.bot_token:
            raise ValueError("Discord bot token is required. Set DISCORD_BOT_TOKEN in .env file")
        if not self.channel_id:
            raise ValueError("Discord channel ID is required. Set DISCORD_CHANNEL_ID in .env file")
        
        self.headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, content: str = None, embed: Dict = None) -> Optional[Dict]:
        """
        Send a message to the configured Discord channel
        
        Args:
            content: Text content of the message (up to 2000 characters)
            embed: Discord embed object (optional)
            
        Returns:
            Response JSON if successful, None otherwise
        """
        if not content and not embed:
            print("Error: Either content or embed must be provided")
            return None
        
        url = f"{self.BASE_URL}/channels/{self.channel_id}/messages"
        
        payload = {}
        if content:
            payload["content"] = content
        if embed:
            payload["embeds"] = [embed]
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            print(f"✅ Message sent successfully to channel {self.channel_id}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"Response: {e.response.text if e.response else 'No response'}")
            return None
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending message: {e}")
            return None
    
    def create_weather_embed(self, weather_message: str) -> Dict:
        """
        Create a Discord embed for weather information
        
        Args:
            weather_message: Formatted weather message string
            
        Returns:
            Discord embed object
        """
        # Parse the weather message to extract key information
        lines = weather_message.split('\n')
        
        # Create a rich embed
        embed = {
            "title": "🌤️ Daily Weather Report",
            "description": "Your morning weather update",
            "color": 0x5865F2,  # Discord blurple color
            "fields": [],
            "footer": {
                "text": "Powered by Open-Meteo API"
            }
        }
        
        # Add the full weather message as a field
        embed["fields"].append({
            "name": "Weather Details",
            "value": weather_message[:1024],  # Discord field value limit
            "inline": False
        })
        
        return embed
    
    def send_weather_update(self, weather_message: str, use_embed: bool = True) -> Optional[Dict]:
        """
        Send a weather update message
        
        Args:
            weather_message: Formatted weather message
            use_embed: Whether to use Discord embed (default: True)
            
        Returns:
            Response JSON if successful, None otherwise
        """
        if use_embed:
            embed = self.create_weather_embed(weather_message)
            return self.send_message(embed=embed)
        else:
            return self.send_message(content=weather_message)
    
    def test_connection(self) -> bool:
        """
        Test the Discord bot connection by fetching channel info
        
        Returns:
            True if connection successful, False otherwise
        """
        url = f"{self.BASE_URL}/channels/{self.channel_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            channel_data = response.json()
            print(f"✅ Successfully connected to channel: {channel_data.get('name', 'Unknown')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection test failed: {e}")
            return False


if __name__ == "__main__":
    # Test the Discord bot
    try:
        bot = DiscordBot()
        print("Testing Discord bot connection...")
        
        if bot.test_connection():
            print("\nSending test message...")
            bot.send_message(content="🤖 Discord bot is online and ready!")
        else:
            print("\n⚠️ Please check your Discord bot token and channel ID in .env file")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n📝 Please update your .env file with:")
        print("   - DISCORD_BOT_TOKEN=your_bot_token_here")
        print("   - DISCORD_CHANNEL_ID=your_channel_id_here")

