#!/usr/bin/env python3
"""
Build ICS calendar from streams.yml data.
Generates static/schedule.ics with future events only.
"""

import yaml
import os
from datetime import datetime
from zoneinfo import ZoneInfo

def load_streams():
    """Load streams from YAML file."""
    try:
        with open('data/streams.yml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('streams', [])
    except FileNotFoundError:
        print("Error: data/streams.yml not found")
        return []
    except Exception as e:
        print(f"Error loading streams.yml: {e}")
        return []

def is_future_event(start_str):
    """Check if event is in the future."""
    try:
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        now = datetime.now(ZoneInfo("Europe/Moscow"))
        return start_dt > now
    except Exception as e:
        print(f"Error parsing date {start_str}: {e}")
        return False

def format_ics_datetime(dt_str):
    """Convert ISO datetime to ICS format (UTC with Z suffix)."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        utc_dt = dt.astimezone(ZoneInfo("UTC"))
        return utc_dt.strftime('%Y%m%dT%H%M%SZ')
    except Exception as e:
        print(f"Error formatting datetime {dt_str}: {e}")
        return ""

def get_localized_field(field, lang='ru'):
    """Get localized field value."""
    if isinstance(field, dict):
        return field.get(lang, field.get('ru', field.get('en', '')))
    return field or ''

def generate_ics(streams):
    """Generate ICS calendar content."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Agents Blog//Stream Schedule//RU",
        "CALSCALE:GREGORIAN"
    ]
    
    future_streams = [s for s in streams if is_future_event(s.get('start', ''))]
    print(f"Found {len(future_streams)} future events")
    
    for stream in future_streams:
        start_ics = format_ics_datetime(stream.get('start', ''))
        end_ics = format_ics_datetime(stream.get('end', ''))
        
        if not start_ics or not end_ics:
            continue
        
        title = get_localized_field(stream.get('title', ''), 'ru')
        desc = get_localized_field(stream.get('desc', ''), 'ru')
            
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{stream.get('id', 'unknown')}@ai-agents-blog",
            f"DTSTART:{start_ics}",
            f"DTEND:{end_ics}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{desc}",
            "END:VEVENT"
        ])
    
    lines.append("END:VCALENDAR")
    return '\n'.join(lines)

def main():
    """Main function."""
    print("Building ICS calendar...")
    
    streams = load_streams()
    if not streams:
        print("No streams found, creating empty calendar")
    
    ics_content = generate_ics(streams)
    
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    
    # Write ICS file
    try:
        with open('static/schedule.ics', 'w', encoding='utf-8') as f:
            f.write(ics_content)
        print("✓ Created static/schedule.ics")
    except Exception as e:
        print(f"Error writing ICS file: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())