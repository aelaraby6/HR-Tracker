from api.config import client

async def fetch_messages(group, target_username, start_date=None, end_date=None):
    count = 0
    messages_list = []

    async for message in client.iter_messages(group):
        if message.sender and message.sender.username == target_username:
            msg_date = message.date.replace(tzinfo=None) 

            if start_date and msg_date < start_date:
                continue
            if end_date and msg_date > end_date:
                continue

            count += 1
            messages_list.append(message)

    return count, messages_list
