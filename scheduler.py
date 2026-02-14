#!/usr/bin/env python3
"""
Scheduler for Discord Weather Bot
Sends weather updates at a specified time daily
"""

import os
import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from main import send_weather_to_discord

# Load environment variables
load_dotenv()


def get_schedule_time():
    """
    Get the scheduled time from environment variable
    
    Returns:
        Tuple of (hour, minute) for scheduling
    """
    weather_time = os.getenv("WEATHER_TIME", "09:00")
    try:
        hour, minute = weather_time.split(":")
        return int(hour), int(minute)
    except (ValueError, AttributeError):
        print(f"⚠️ Invalid WEATHER_TIME format: {weather_time}, using default 09:00")
        return 9, 0


def scheduled_weather_update():
    """Wrapper function for scheduled weather updates"""
    print("\n" + "=" * 60)
    print(f"⏰ Scheduled weather update triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    success = send_weather_to_discord()
    
    if success:
        print("=" * 60)
        print("✅ Scheduled weather update completed successfully!")
        print(f"⏰ Next update scheduled for tomorrow at {get_schedule_time()[0]:02d}:{get_schedule_time()[1]:02d}")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ Scheduled weather update failed!")
        print("=" * 60)


def start_scheduler():
    """Start the scheduler for daily weather updates"""
    hour, minute = get_schedule_time()
    
    print("🤖 Discord Weather Bot - Scheduler Starting")
    print("=" * 60)
    print(f"📅 Daily weather updates scheduled for: {hour:02d}:{minute:02d}")
    print(f"📍 Location: {os.getenv('LATITUDE')}, {os.getenv('LONGITUDE')}")
    print(f"💬 Discord Channel ID: {os.getenv('DISCORD_CHANNEL_ID', 'Not configured')}")
    print("=" * 60)
    
    # Create scheduler
    scheduler = BlockingScheduler()
    
    # Schedule the job to run daily at the specified time
    scheduler.add_job(
        scheduled_weather_update,
        trigger=CronTrigger(hour=hour, minute=minute),
        id='daily_weather_update',
        name='Daily Weather Update',
        replace_existing=True
    )
    
    # Calculate time until next run
    now = datetime.now()
    next_run = scheduler.get_jobs()[0].next_run_time
    time_until = next_run - now
    
    print(f"⏰ Next weather update: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏳ Time until next update: {time_until}")
    print("=" * 60)
    print("✅ Scheduler is running... Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Start the scheduler
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n" + "=" * 60)
        print("🛑 Scheduler stopped by user")
        print("=" * 60)
        scheduler.shutdown()


def run_immediate_test():
    """Run an immediate test before starting the scheduler"""
    print("\n🧪 Running immediate test before starting scheduler...")
    print("=" * 60)
    
    success = send_weather_to_discord()
    
    if success:
        print("\n✅ Test successful! Starting scheduler...")
        time.sleep(2)
        return True
    else:
        print("\n❌ Test failed! Please fix the issues before starting the scheduler.")
        print("💡 Tip: Check your .env file configuration")
        return False


if __name__ == "__main__":
    import sys
    
    # Check if user wants to skip the test
    skip_test = "--no-test" in sys.argv or "-n" in sys.argv
    immediate = "--now" in sys.argv
    
    if immediate:
        # Just run once immediately
        print("🚀 Running weather update immediately...")
        send_weather_to_discord()
    elif skip_test:
        # Skip test and start scheduler directly
        print("⚠️ Skipping initial test...")
        start_scheduler()
    else:
        # Run test first, then start scheduler
        if run_immediate_test():
            start_scheduler()
        else:
            print("\n❌ Scheduler not started due to test failure")
            sys.exit(1)

