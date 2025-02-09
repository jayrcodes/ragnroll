import pydash
import json
from utils.slack import users

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

    print("\nUsers saved to data/slack_users.json\n")

main()
