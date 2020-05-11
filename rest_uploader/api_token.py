from os import path


def get_token():
    if path.exists(".api_token.txt"):
        with open(".api_token.txt", "r") as f:
            token = f.readline().rstrip()
    else:
        token = input("Paste your Joplin API Token:")
        with open(".api_token.txt", "w") as f:
            f.write(token.rstrip())
    return token


def get_token_suffix():
    return "?token=" + get_token()


"""
Code from a non-Joplin API
Not currently used
"""

"""
import requests

def get_header():
    try:
        my_token = get_token()
        url = SERVER + "/ping"
        head = {"Authorization": f"Bearer {my_token}"}
        try:
            response = requests.get(url, headers=head)
            if response.status_code != 200:
                print("Invalid token!")
        except ValueError:
            print("Token expired!")
    except FileNotFoundError:
        print("No Token!")
    return head
"""
