import pydash
import json
from utils.slack import users
from utils.error import try_catch, print_exit_if_error

def main():
    [response, error] = try_catch(users)
    print_exit_if_error(error)

    def write_users():
        members = []

        for member in response['members']:
            members.append({
                'id': member['id'],
                'real_name': pydash.get(member, 'profile.real_name')
            })

        pretty = json.dumps(members, indent=4)

        with open('data/slack_users.json', 'w') as file:
            file.write(pretty)

    [_, error] = try_catch(write_users)
    print_exit_if_error(error)

    print("\nUsers saved to data/slack_users.json\n")

main()
