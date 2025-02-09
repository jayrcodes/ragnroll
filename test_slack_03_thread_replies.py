import json
import pydash
import re
from utils.error import try_catch, print_exit_if_error
from utils.slack import conversation_replies

def get_thread_messages():
    def get_slack_curl(): return open('data/slack_curl.txt', 'r').read()
    [slack_curl, error] = try_catch(get_slack_curl)
    print_exit_if_error(error)

    def get_channel_id(): return re.search(r'\"channel\"\\r\\n\\r\\n([A-Z0-9]+)', slack_curl).group(1)  
    [channel_id, error] = try_catch(get_channel_id)
    print_exit_if_error(error)

    def get_ts(): return re.search(r'\"ts\"\\r\\n\\r\\n([0-9.]+)', slack_curl).group(1)
    [ts, error] = try_catch(get_ts)
    print_exit_if_error(error)

    # channel_id = pydash.get(sys.argv, 1)
    # if not channel_id:
    #     raise ValueError("Channel ID is required")

    # ts = pydash.get(sys.argv, 2)
    # if not ts:
    #     raise ValueError("Thread timestamp is required")

    [data, error] = try_catch(lambda: conversation_replies(channel_id=channel_id, ts=ts))
    print_exit_if_error(error)

    def get_users(): return json.load(open('data/slack_users.json', 'r'))       
    [users, error] = try_catch(get_users)
    print_exit_if_error(error)

    def write_thread_messages():
        with open('data/slack_thread_messages.txt', 'w') as file:
            file.write('')

    [_, error] = try_catch(write_thread_messages)
    print_exit_if_error(error)

    def write_thread_messages():
        for message in data['messages']:
            name = next((user for user in users if user['id'] == message['user']), None)
            name = pydash.get(name, 'real_name') or message['user']

            with open('data/slack_thread_messages.txt', 'a') as file:
                file.write(name + ":")
                file.write(message['text'] + "\n")

    [_, error] = try_catch(write_thread_messages)
    print_exit_if_error(error)

    print("\nDone. Check data/slack_thread_messages.txt\n")

get_thread_messages()
