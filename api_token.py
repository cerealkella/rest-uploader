import requests
from os import path
from settings import SERVER


def get_token():
    with open(".api_token.txt", "r") as f:
        token = f.readline().rstrip()
        return token


def get_token_suffix():
    return "?token=" + get_token()


# Code from a non-Joplin API
def get_header():
    try:
        my_token = get_token()
        url = SERVER + "/ping"
        head = {"Authorization": "Bearer {}".format(my_token)}
        try:
            response = requests.get(url, headers=head)
            if response.status_code != 200:
                print("Invalid token!")
        except ValueError:
            print("Token expired!")
    except FileNotFoundError:
        print("No Token!")
    return head
