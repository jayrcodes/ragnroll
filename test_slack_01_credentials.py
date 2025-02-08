import re

def write_credentials():
    slack_curl = open('data/slack_curl.txt', 'r').read()

    # cookie:
    cookie = re.search(r'\'cookie:(.*)\\', slack_curl).group(1)
    # trim
    cookie = cookie.strip()

    # append to .env as SLACK_COOKIE
    with open('.env', 'a') as file:
        file.write(f"\nSLACK_COOKIE=\"{cookie}\"\n")

    token = re.search(r'\"token\"\\r\\n\\r\\n(.*?)(?=\\r\\n)', slack_curl).group(1)
    # append to .env as SLACK_API_TOKEN
    with open('.env', 'a') as file:
        file.write(f"\nSLACK_API_TOKEN=\"{token}\"\n")


write_credentials()
