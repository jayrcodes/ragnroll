import requests
import sys
import json
import pydash
import re
from utils.config import SLACK_API_ENDPOINT, SLACK_API_TOKEN, SLACK_COOKIE


def conversation_replies(channel_id, ts):
    url = f"{SLACK_API_ENDPOINT}/api/conversations.replies"

    params = {
        "pretty": 1,
        "channel": channel_id,
        "ts": ts,
    }

    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
        "Cookie": SLACK_COOKIE,
        "Content-Type": "application/json; charset=utf-8",
    }

    body = {
        "token": SLACK_API_TOKEN,
    }

    response = requests.post(url, json=body, headers=headers, params=params)

    return response.json()

def main():
    slack_curl = open('data/slack_curl.txt', 'r').read()

    channel_id = re.search(r'\"channel\"\\r\\n\\r\\n([A-Z0-9]+)', slack_curl).group(1)
    ts = re.search(r'\"ts\"\\r\\n\\r\\n([0-9.]+)', slack_curl).group(1)

    # channel_id = pydash.get(sys.argv, 1)
    # if not channel_id:
    #     raise ValueError("Channel ID is required")

    # ts = pydash.get(sys.argv, 2)
    # if not ts:
    #     raise ValueError("Thread timestamp is required")

    data = conversation_replies(channel_id=channel_id, ts=ts)

    users = json.load(open('data/slack_users.json', 'r'))

    # clear data/slack_thread_messages.txt
    with open('data/slack_thread_messages.txt', 'w') as file:
        file.write('')

    for message in data['messages']:
        # find by array
        name = next((user for user in users if user['id'] == message['user']), None)
        name = pydash.get(name, 'real_name') or message['user']

        # print(name + ":")
        # print(message['text'] + "\n")

        # write to data/slack_thread_messages.txt
        with open('data/slack_thread_messages.txt', 'a') as file:
            file.write(name + ":")
            file.write(message['text'] + "\n")

    print("Done. Check data/slack_thread_messages.txt")

main()
