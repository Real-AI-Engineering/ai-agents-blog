#!/usr/bin/env python3
"""
Post weekly stream schedule to Discord webhook.
Collects streams for next 7 days and sends formatted message.
"""

import yaml
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def load_streams():
    """Load streams from YAML file."""
    try:
        with open('data/streams.yml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('streams', [])
    except Exception as e:
        print(f"Error loading streams.yml: {e}")
        return []

def get_localized_field(field, lang='ru'):
    """Get localized field value."""
    if isinstance(field, dict):
        return field.get(lang, field.get('ru', field.get('en', '')))
    return field or ''

def is_in_next_7_days(start_str):
    """Check if event is within next 7 days."""
    try:
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        moscow_tz = ZoneInfo("Europe/Moscow")
        start_moscow = start_dt.astimezone(moscow_tz)
        
        now_moscow = datetime.now(moscow_tz)
        week_later = now_moscow + timedelta(days=7)
        
        return now_moscow <= start_moscow <= week_later
    except Exception as e:
        print(f"Error parsing date {start_str}: {e}")
        return False

def format_stream_time(start_str):
    """Format stream time as dd.MM (Day) HH:mm МСК."""
    try:
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        moscow_tz = ZoneInfo("Europe/Moscow")
        start_moscow = start_dt.astimezone(moscow_tz)
        
        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        day_name = weekdays[start_moscow.weekday()]
        
        return f"{start_moscow.strftime('%d.%m')} ({day_name}) {start_moscow.strftime('%H:%M')} МСК"
    except Exception as e:
        print(f"Error formatting date {start_str}: {e}")
        return "Дата неизвестна"

def build_message(streams):
    """Build Discord message with stream schedule."""
    if not streams:
        return "📅 **Расписание стримов на неделю**\n\nСтримов на ближайшую неделю не запланировано."
    
    lines = ["📅 **Расписание стримов на неделю**\n"]
    
    # Sort streams by start time
    sorted_streams = sorted(streams, key=lambda s: s.get('start', ''))
    
    for stream in sorted_streams:
        time_str = format_stream_time(stream.get('start', ''))
        title = get_localized_field(stream.get('title', ''), 'ru')
        desc = get_localized_field(stream.get('desc', ''), 'ru').strip()
        
        line = f"🔴 **{time_str}** — {title}"
        
        # Add platforms
        links = stream.get('links', {})
        platforms = []
        if links.get('twitch'):
            platforms.append("[Twitch](twitch)")
        if links.get('youtube'):
            platforms.append("[YouTube](youtube)")
        if platforms:
            line += f" ({', '.join(platforms)})"
        
        lines.append(line)
        
        # Add description if available
        if desc:
            lines.append(f"   {desc}")
        
        lines.append("")  # Empty line between streams
    
    # Add footer with link to full schedule
    site_url = os.getenv('SITE_PUBLIC_URL', 'https://real-ai-engineering.github.io/ai-agents-blog')
    lines.append(f"Подробнее: {site_url}/ru/schedule/")
    
    return "\n".join(lines)

def send_discord_message(message):
    """Send message to Discord webhook."""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("! DISCORD_WEBHOOK_URL not set")
        return False
    
    data = {
        "content": message,
        "username": "AI Agents Stream Bot"
    }
    
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("✓ Message sent to Discord")
                return True
            else:
                print(f"! Discord webhook returned status {response.status}")
                return False
    except Exception as e:
        print(f"Discord webhook error: {e}")
        return False

def main():
    """Main function."""
    print("Posting stream schedule to Discord...")
    
    streams = load_streams()
    if not streams:
        print("No streams found")
        return 0
    
    # Filter streams for next 7 days
    upcoming_streams = [s for s in streams if is_in_next_7_days(s.get('start', ''))]
    
    print(f"Found {len(upcoming_streams)} streams in next 7 days")
    
    message = build_message(upcoming_streams)
    print(f"Message preview:\n{message[:200]}...")
    
    if send_discord_message(message):
        print("✓ Schedule posted to Discord")
        return 0
    else:
        print("! Failed to post to Discord")
        return 1

if __name__ == '__main__':
    exit(main())