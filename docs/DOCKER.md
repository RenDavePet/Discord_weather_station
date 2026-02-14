# Docker Deployment Guide

## Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)

## Quick Start with Docker

### 1. Configure Environment Variables

Make sure your `src/.env` file is configured (copy from `src/.env.example` if needed):

```env
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
LATITUDE=your_latitude
LONGITUDE=your_longitude
WEATHER_TIME=09:00
```

### 2. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down

# Restart the bot
docker-compose restart
```

### 3. Or Use Docker Commands Directly

**Build the image:**
```bash
docker build -t discord-weather-bot .
```

**Run the container:**
```bash
docker run -d \
  --name discord-weather-bot \
  --env-file .env \
  --restart unless-stopped \
  discord-weather-bot
```

**View logs:**
```bash
docker logs -f discord-weather-bot
```

**Stop the container:**
```bash
docker stop discord-weather-bot
```

**Remove the container:**
```bash
docker rm discord-weather-bot
```

## Docker Compose Commands

### Start the bot
```bash
docker-compose up -d
```
- `-d` runs in detached mode (background)

### View real-time logs
```bash
docker-compose logs -f
```
- `-f` follows the log output
- Press `Ctrl+C` to exit (bot keeps running)

### Check bot status
```bash
docker-compose ps
```

### Restart the bot
```bash
docker-compose restart
```

### Stop the bot
```bash
docker-compose down
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

### View last 100 log lines
```bash
docker-compose logs --tail=100
```

## Testing Before Deployment

### Test with immediate weather update
```bash
docker-compose run --rm weather-bot python scheduler.py --now
```

### Test with initial test + scheduler
```bash
docker-compose run --rm weather-bot python scheduler.py
```
Press `Ctrl+C` to stop after the test

## Timezone Configuration

The bot uses the timezone set in `docker-compose.yml`. To change it:

1. Edit `docker-compose.yml`
2. Change the `TZ` environment variable:
   ```yaml
   environment:
     - TZ=Europe/Paris  # Change to your timezone
   ```

Common timezones:
- `Europe/Paris`
- `America/New_York`
- `America/Los_Angeles`
- `Asia/Tokyo`
- `UTC`

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Automatic Restart

The bot is configured with `restart: unless-stopped` which means:
- ✅ Restarts automatically if it crashes
- ✅ Starts automatically when Docker starts
- ✅ Starts automatically after system reboot
- ❌ Won't restart if you manually stop it with `docker-compose down`

## Updating the Bot

When you make changes to the code:

```bash
# Stop the current container
docker-compose down

# Rebuild the image with new code
docker-compose build

# Start with new image
docker-compose up -d

# Or do it all in one command
docker-compose up -d --build
```

## Troubleshooting

### Bot not starting
```bash
# Check logs for errors
docker-compose logs

# Check if container is running
docker-compose ps
```

### Environment variables not working
```bash
# Make sure .env file exists and has correct values
cat .env

# Restart after changing .env
docker-compose down
docker-compose up -d
```

### Time is wrong in logs
- Set the correct timezone in `docker-compose.yml`
- Rebuild and restart: `docker-compose up -d --build`

### Want to see what's happening inside the container
```bash
# Open a shell in the running container
docker-compose exec weather-bot /bin/bash

# Or if the container isn't running
docker-compose run --rm weather-bot /bin/bash
```

## Production Deployment

### On a VPS/Cloud Server

1. Install Docker and Docker Compose
2. Clone your repository or copy files
3. Configure `.env` file
4. Run: `docker-compose up -d`
5. Check logs: `docker-compose logs -f`

### On Raspberry Pi

Same as VPS, but make sure to:
1. Use a 64-bit OS for better compatibility
2. The image will build for ARM architecture automatically

### Monitoring

Check if bot is running:
```bash
docker-compose ps
```

View recent logs:
```bash
docker-compose logs --tail=50
```

Follow logs in real-time:
```bash
docker-compose logs -f
```

## Security Notes

- ✅ The container runs as a non-root user (`botuser`)
- ✅ `.env` file is not copied into the image (passed at runtime)
- ✅ Minimal base image (Python slim)
- ✅ No unnecessary packages installed

## Advantages of Docker Deployment

✅ **Isolated environment** - No conflicts with system Python
✅ **Consistent** - Works the same everywhere
✅ **Easy updates** - Just rebuild and restart
✅ **Auto-restart** - Recovers from crashes automatically
✅ **Portable** - Deploy anywhere Docker runs
✅ **Clean** - Easy to remove completely

