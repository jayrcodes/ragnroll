import requests
import pydash
import json
from utils.config import SLACK_API_ENDPOINT, SLACK_API_TOKEN, SLACK_COOKIE

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


def main():
    response = users()

    members = []

    for member in response['members']:
        members.append({
            'id': member['id'],
            'real_name': pydash.get(member, 'profile.real_name')
        })

    pretty = json.dumps(members, indent=4)

    with open('data/slack_users.json', 'w') as file:
        file.write(pretty)


main()
