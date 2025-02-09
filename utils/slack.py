import requests
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

def users():
    url = f"{SLACK_API_ENDPOINT}/api/users.list"

    params = {
        "pretty": 1,
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