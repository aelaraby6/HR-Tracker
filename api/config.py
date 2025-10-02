import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("hr_session", api_id, api_hash)


# Export the credentials so they can be used in other threads
__all__ = ['client', 'api_id', 'api_hash']