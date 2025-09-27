# api/api_call.py
import re
from telethon import TelegramClient

async def get_messages(group_identifier, username):
    """Get messages from a group for a specific user"""
    try:
        # Clean the group identifier
        group_identifier = clean_telegram_identifier(group_identifier)
        
        # Clean the username
        username = clean_username(username)
        
        print(f"Searching for group: {group_identifier}")
        print(f"Searching for user: {username}")
        
        # Your existing code here...
        
    except Exception as e:
        print(f"Error in get_messages: {e}")
        raise e

def clean_telegram_identifier(identifier):
    """Clean Telegram group identifier"""
    if not identifier:
        return identifier
    
    # Remove any display name part if present
    if ' (' in identifier and identifier.endswith(')'):
        identifier = identifier.split(' (')[-1].rstrip(')')
    
    # Extract username from URL
    if identifier.startswith('https://t.me/'):
        identifier = identifier.replace('https://t.me/', '')
        if identifier.startswith('+'):
            return identifier  # Private group invite code
        else:
            return '@' + identifier.split('/')[0]
    elif identifier.startswith('t.me/'):
        identifier = identifier.replace('t.me/', '')
        if identifier.startswith('+'):
            return identifier
        else:
            return '@' + identifier.split('/')[0]
    elif not identifier.startswith('@'):
        return '@' + identifier
    else:
        return identifier

def clean_username(username):
    """Clean Telegram username"""
    if not username:
        return username
    
    if username.startswith('@'):
        return username[1:]
    return username