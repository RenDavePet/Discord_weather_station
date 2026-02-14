# Discord Weather Bot Setup Guide

## Prerequisites
- Python 3.8 or higher
- A Discord account
- A Discord server where you have admin permissions

## Step 1: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give your application a name (e.g., "Weather Bot")
4. Go to the "Bot" tab on the left sidebar
5. Click "Add Bot" and confirm
6. Under the bot's username, click "Reset Token" and copy the token
   - ⚠️ **Keep this token secret!** Never share it or commit it to git

## Step 2: Get Bot Permissions

1. Still in the "Bot" tab, scroll down to "Privileged Gateway Intents"
2. Enable "MESSAGE CONTENT INTENT" (optional, but recommended)
3. Go to the "OAuth2" > "URL Generator" tab
4. Under "Scopes", select:
   - `bot`
5. Under "Bot Permissions", select:
   - `Send Messages`
   - `Embed Links`
   - `Read Message History`
6. Copy the generated URL at the bottom
7. Paste it in your browser and invite the bot to your server

## Step 3: Get Your Channel ID

1. Open Discord and enable Developer Mode:
   - User Settings > App Settings > Advanced > Developer Mode (toggle ON)
2. Right-click on the channel where you want weather updates
3. Click "Copy Channel ID"

## Step 4: Configure the Bot

1. Copy `src/.env.example` to `src/.env`
2. Open the `src/.env` file
3. Replace the placeholder values with your actual credentials:

```env
DISCORD_BOT_TOKEN=your_actual_bot_token_here
DISCORD_CHANNEL_ID=your_actual_channel_id_here
LATITUDE=your_latitude_here
LONGITUDE=your_longitude_here
WEATHER_TIME=09:00
```

**Note:** You can find your coordinates at [latlong.net](https://www.latlong.net/)

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Test the Bot

### Test Weather Fetching
```bash
python weather.py
```

### Test Discord Connection
```bash
python discord_bot.py
```

### Test Full Integration
```bash
python main.py
```

If everything works, you should see:
- Weather data printed to console
- A message sent to your Discord channel

## Step 7: Run the Scheduler

Once the bot is working, you can start the scheduler for automatic daily updates.

### Option 1: Run with Initial Test (Recommended)
```bash
python scheduler.py
```
This will:
1. Send an immediate test message to verify everything works
2. Start the scheduler for daily updates at 9 AM

### Option 2: Run Immediately (One-time)
```bash
python scheduler.py --now
```
Sends weather update once and exits (useful for testing)

### Option 3: Skip Initial Test
```bash
python scheduler.py --no-test
```
Starts the scheduler without sending a test message first

### Keep the Bot Running 24/7

The scheduler needs to keep running to send daily updates. Options:

**On Windows:**
- Keep the terminal window open
- Or use Task Scheduler to run on startup

**On Linux/Mac:**
- Use `screen` or `tmux` to run in background
- Or create a systemd service (see below)

**On Raspberry Pi / Server:**
- Use systemd service (recommended for 24/7 operation)

### Create a Systemd Service (Linux)

Create `/etc/systemd/system/weather-bot.service`:

```ini
[Unit]
Description=Discord Weather Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/Discord_weather_station
ExecStart=/usr/bin/python3 /path/to/Discord_weather_station/scheduler.py --no-test
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable weather-bot
sudo systemctl start weather-bot
sudo systemctl status weather-bot
```

## Troubleshooting

### "Discord bot token is required"
- Make sure you've added your bot token to the `.env` file
- Check that there are no extra spaces or quotes around the token

### "403 Forbidden" or "Missing Permissions"
- Make sure the bot has been invited to your server
- Check that the bot has "Send Messages" permission in the channel
- Verify the channel ID is correct

### "404 Not Found"
- Double-check your channel ID
- Make sure the bot is in the same server as the channel

### Weather data not fetching
- Check your internet connection
- The Open-Meteo API might be temporarily down (rare)

## Security Notes

- ✅ The `.env` file is in `.gitignore` - your token is safe
- ❌ Never commit your `.env` file to git
- ❌ Never share your bot token publicly
- ✅ If your token is leaked, reset it immediately in the Discord Developer Portal

