# 🌤️ Discord Weather Bot

A Discord bot that sends daily weather updates at 9 AM using the Open-Meteo API. Built with Python, using only `requests` for HTTP calls (no Discord API wrappers).

## ✨ Features

- 🌡️ **Daily weather updates** at a configurable time (default: 9 AM)
- 📍 **Location-based forecasts** using coordinates
- 🎨 **Beautiful Discord embeds** with weather information
- 🔒 **Secure** - Credentials stored in `.env` file
- 🐳 **Docker support** - Easy deployment with Docker Compose
- 🔄 **Auto-restart** - Recovers from crashes automatically
- 📊 **Detailed weather data**:
  - Current temperature and "feels like"
  - Humidity and wind speed
  - Weather conditions with emojis
  - Daily high/low temperatures
  - Precipitation forecast

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Configure your `src/.env` file:**
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   DISCORD_CHANNEL_ID=your_channel_id_here
   LATITUDE=your_latitude
   LONGITUDE=your_longitude
   WEATHER_TIME=09:00
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

See [DOCKER.md](docs/DOCKER.md) for detailed Docker instructions.

### Option 2: Python (Local)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env` file** (same as above)

3. **Run the scheduler:**
   ```bash
   python scheduler.py
   ```

See [SETUP.md](docs/SETUP.md) for detailed setup instructions.

## 📋 Prerequisites

### For Docker:
- Docker and Docker Compose installed
- Discord bot token and channel ID

### For Python:
- Python 3.8 or higher
- Discord bot token and channel ID

## 🔧 Configuration

All configuration is done via the `src/.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | `MTIzNDU2Nzg5...` |
| `DISCORD_CHANNEL_ID` | Channel ID to send messages | `123456789012345678` |
| `LATITUDE` | Your location latitude | `48.8566` |
| `LONGITUDE` | Your location longitude | `2.3522` |
| `WEATHER_TIME` | Time to send daily updates (24h) | `09:00` |

### Getting Discord Credentials

1. Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Copy the bot token
3. Invite bot to your server with "Send Messages" permission
4. Enable Developer Mode in Discord and copy channel ID

See [SETUP.md](docs/SETUP.md) for step-by-step instructions.

## 📁 Project Structure

```
WeatherStation/
├── src/
│   ├── weather.py          # Weather fetching from Open-Meteo API
│   ├── discord_bot.py      # Discord API integration
│   ├── main.py             # Integration script
│   ├── scheduler.py        # Daily scheduler
│   ├── .env                # Your credentials (create from .env.example)
│   └── .env.example        # Template for .env
├── docs/
│   ├── SETUP.md            # Detailed setup guide
│   └── DOCKER.md           # Docker deployment guide
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🐳 Docker Commands

```bash
# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down

# Restart the bot
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build
```

## 🧪 Testing

```bash
# Test weather fetching
python weather.py

# Test Discord connection
python discord_bot.py

# Test full integration
python main.py

# Send weather update immediately (one-time)
python scheduler.py --now
```

## 📚 Documentation

- [SETUP.md](docs/SETUP.md) - Detailed setup instructions
- [DOCKER.md](docs/DOCKER.md) - Docker deployment guide
- [QUICK_START.md](QUICK_START.md) - Quick reference guide

## 🛠️ Tech Stack

- **Python 3.11** - Programming language
- **requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **APScheduler** - Task scheduling
- **Open-Meteo API** - Weather data source
- **Discord API v10** - Message sending (no wrappers)
- **Docker** - Containerization

## 🔒 Security

- ✅ Credentials stored in `.env` file (not committed to git)
- ✅ Docker container runs as non-root user
- ✅ Minimal dependencies
- ✅ No API wrappers - direct HTTP calls only

## 📝 License

This project is provided "AS-IS" without any warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

This project is open source and available for personal use.

## 🤝 Contributing

Feel free to fork, modify, and use this project for your own needs!

## ⚠️ Troubleshooting

**Bot not sending messages?**
- Check your bot token and channel ID in `.env`
- Verify the bot is invited to your server
- Ensure the bot has "Send Messages" permission

**Weather data not loading?**
- Check your internet connection
- Verify latitude/longitude are correct

**Docker container not starting?**
- Check logs: `docker-compose logs`
- Verify `.env` file exists and is configured

See [SETUP.md](docs/SETUP.md) for more troubleshooting tips.
