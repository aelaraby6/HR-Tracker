import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("hr_session", api_id, api_hash)

async def main():
    group = "https://t.me/+cRpa24PglDg2OTY0"
    target_username = "ABDoooo_abdo"
    
    count = 0
    messages_list = []

    async for message in client.iter_messages(group):
        if message.sender and message.sender.username == target_username:
            count += 1
            if message.text:
                messages_list.append(message.text)

    with open("messages.txt", "w", encoding="utf-8") as f:
        for msg in messages_list:
            f.write(msg + "\n" + "-"*40 + "\n")

    print(f"messages number : @{target_username} = {count}")
    print("messages saved in m.txt")

with client:
    client.loop.run_until_complete(main())
