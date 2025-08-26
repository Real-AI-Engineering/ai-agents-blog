#!/usr/bin/env python3
"""
Generate AI descriptions for streams scheduled tomorrow.
Supports OpenAI (gpt-4o-mini) and Anthropic (claude-3-haiku-20240307).
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
        return data
    except Exception as e:
        print(f"Error loading streams.yml: {e}")
        return None

def save_streams(data):
    """Save streams back to YAML file."""
    try:
        with open('data/streams.yml', 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        print("✓ Updated streams.yml")
    except Exception as e:
        print(f"Error saving streams.yml: {e}")

def get_localized_field(field, lang='ru'):
    """Get localized field value."""
    if isinstance(field, dict):
        return field.get(lang, field.get('ru', field.get('en', '')))
    return field or ''

def is_tomorrow(start_str):
    """Check if event is scheduled for tomorrow (Europe/Moscow timezone)."""
    try:
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        moscow_tz = ZoneInfo("Europe/Moscow")
        start_moscow = start_dt.astimezone(moscow_tz)
        
        now_moscow = datetime.now(moscow_tz)
        tomorrow = now_moscow.date() + timedelta(days=1)
        
        return start_moscow.date() == tomorrow
    except Exception as e:
        print(f"Error parsing date {start_str}: {e}")
        return False

def call_openai_api(title, tags, lang='ru'):
    """Call OpenAI API for description generation."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    
    if lang == 'ru':
        prompt = f"Создай краткое описание для стрима '{title}' с тегами {tags}. 2-3 предложения на русском языке. Без лишних слов, конкретно о том, что будет в стриме."
    else:
        prompt = f"Create a brief description for the stream '{title}' with tags {tags}. 2-3 sentences in English. Be specific about what will be covered in the stream."
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def call_anthropic_api(title, tags, lang='ru'):
    """Call Anthropic API for description generation."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return None
    
    if lang == 'ru':
        prompt = f"Создай краткое описание для стрима '{title}' с тегами {tags}. 2-3 предложения на русском языке. Без лишних слов, конкретно о том, что будет в стриме."
    else:
        prompt = f"Create a brief description for the stream '{title}' with tags {tags}. 2-3 sentences in English. Be specific about what will be covered in the stream."
    
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 150,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(data).encode('utf-8'),
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['content'][0]['text'].strip()
    except Exception as e:
        print(f"Anthropic API error: {e}")
        return None

def generate_description(title, tags, lang='ru'):
    """Generate description using available AI API."""
    # Try OpenAI first
    desc = call_openai_api(title, tags, lang)
    if desc:
        print(f"✓ Generated {lang.upper()} description via OpenAI")
        return desc
    
    # Try Anthropic if OpenAI failed
    desc = call_anthropic_api(title, tags, lang)
    if desc:
        print(f"✓ Generated {lang.upper()} description via Anthropic")
        return desc
    
    print("! No AI API keys available")
    return None

def main():
    """Main function."""
    print("Checking for streams needing AI descriptions...")
    
    data = load_streams()
    if not data or 'streams' not in data:
        print("No streams data found")
        return 0
    
    updated = False
    streams = data['streams']
    
    for stream in streams:
        # Check if stream is tomorrow and has empty description
        desc_field = stream.get('desc', '')
        ru_desc = get_localized_field(desc_field, 'ru')
        en_desc = get_localized_field(desc_field, 'en')
        
        if is_tomorrow(stream.get('start', '')) and (not ru_desc.strip() or not en_desc.strip()):
            title = get_localized_field(stream.get('title', ''), 'ru')
            tags = stream.get('tags', [])
            
            print(f"Generating description for: {title}")
            
            # Generate Russian description if missing
            if not ru_desc.strip():
                ru_desc = generate_description(title, tags)
                if ru_desc:
                    if isinstance(stream.get('desc'), dict):
                        stream['desc']['ru'] = ru_desc
                    else:
                        stream['desc'] = {'ru': ru_desc, 'en': ''}
                    updated = True
                    print(f"✓ Added RU description: {ru_desc[:50]}...")
            
            # Generate English description if missing
            if not en_desc.strip():
                en_title = get_localized_field(stream.get('title', ''), 'en')
                en_desc = generate_description(en_title, tags, lang='en')
                if en_desc:
                    if isinstance(stream.get('desc'), dict):
                        stream['desc']['en'] = en_desc
                    else:
                        stream['desc'] = {'ru': stream.get('desc', ''), 'en': en_desc}
                    updated = True
                    print(f"✓ Added EN description: {en_desc[:50]}...")
            
            if not ru_desc and not en_desc:
                print(f"! Could not generate description for: {title}")
    
    if updated:
        save_streams(data)
        print("✓ Descriptions updated")
    else:
        print("• No descriptions needed")
    
    return 0

if __name__ == '__main__':
    exit(main())