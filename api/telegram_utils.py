from api.config import client

async def fetch_messages(group, target_username):
    count = 0
    messages_list = []

    async for message in client.iter_messages(group):
        if message.sender and message.sender.username == target_username:
            count += 1
            messages_list.append(message)
    return count, messages_list
