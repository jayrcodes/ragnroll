import json
import pydash
import re
from utils.error import try_with_ai
from utils.slack import conversation_replies

def get_thread_messages():
    def get_slack_curl(): return open('data/slack_curl.txt', 'r').read()
    slack_curl = try_with_ai(get_slack_curl)

    def get_channel_id(): return re.search(r'\"channel\"\\r\\n\\r\\n([A-Z0-9]+)', slack_curl).group(1)  
    channel_id = try_with_ai(get_channel_id)

    def get_ts(): return re.search(r'\"ts\"\\r\\n\\r\\n([0-9.]+)', slack_curl).group(1)
    ts = try_with_ai(get_ts)

    # channel_id = pydash.get(sys.argv, 1)
    # if not channel_id:
    #     raise ValueError("Channel ID is required")

    # ts = pydash.get(sys.argv, 2)
    # if not ts:
    #     raise ValueError("Thread timestamp is required")

    data = try_with_ai(lambda: conversation_replies(channel_id=channel_id, ts=ts))

    def get_users(): return json.load(open('data/slack_users.json', 'r'))       
    users = try_with_ai(get_users)

    def write_thread_messages():
        with open('data/slack_thread_messages.txt', 'w') as file:
            file.write('')
    try_with_ai(write_thread_messages)

    def write_thread_messages():
        for message in data['messages']:
            name = next((user for user in users if user['id'] == message['user']), None)
            name = pydash.get(name, 'real_name') or message['user']

            with open('data/slack_thread_messages.txt', 'a') as file:
                file.write(name + ":")
                file.write(message['text'] + "\n")

    try_with_ai(write_thread_messages)

    print("Done. Check data/slack_thread_messages.txt")

get_thread_messages()
