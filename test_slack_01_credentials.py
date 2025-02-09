import re
from utils.error import try_with_ai

def write_credentials():
    slack_curl = open('data/slack_curl.txt', 'r').read()

    def get_cookie(): return re.search(r'\'cookie:(.*)\\', slack_curl).group(1).strip()
    cookie = try_with_ai(get_cookie)

    def write_cookie():
        with open('.env', 'a') as file:
            file.write(f"\nSLACK_COOKIE=\"{cookie}\"\n")
    try_with_ai(write_cookie)

    def get_token(): return re.search(r'\"token\"\\r\\n\\r\\n(.*?)(?=\\r\\n)', slack_curl).group(1).strip()
    token = try_with_ai(get_token)

    def write_token():
        with open('.env', 'a') as file:
            file.write(f"\nSLACK_API_TOKEN=\"{token}\"\n")
    try_with_ai(write_token)

    print("\nCredentials written to .env")

write_credentials()
