import re
from utils.error import try_catch, print_exit_if_error

def write_credentials():
    def get_slack_curl():
        content = open('data/slack_curl.txt', 'r').read()
        if not content:
            raise Exception("slack_curl.txt is empty")

        return content

    [slack_curl, error] = try_catch(get_slack_curl)
    print_exit_if_error(error)

    def get_cookie(): return re.search(r'\'cookie:(.*)\\', slack_curl).group(1).strip()

    [cookie, error] = try_catch(get_cookie)
    print_exit_if_error(error)

    def write_cookie():
        with open('.env', 'a') as file:
            file.write(f"\nSLACK_COOKIE=\"{cookie}\"\n")

    [_, error] = try_catch(write_cookie)
    print_exit_if_error(error)

    def get_token(): return re.search(r'\"token\"\\r\\n\\r\\n(.*?)(?=\\r\\n)', slack_curl).group(1).strip()
    [token, error] = try_catch(get_token)
    print_exit_if_error(error)

    def write_token():
        with open('.env', 'a') as file:
            file.write(f"\nSLACK_API_TOKEN=\"{token}\"\n")

    [_, error] = try_catch(write_token)
    print_exit_if_error(error)

    print("\nCredentials written to .env")

write_credentials()
