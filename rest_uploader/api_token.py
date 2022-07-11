import sys
import pathlib


def get_os_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """
    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


def get_my_datadir() -> pathlib.Path:
    """Find datadir, create it if it doesn't exist"""
    my_datadir = get_os_datadir() / __package__
    try:
        my_datadir.mkdir(parents=True)
    except FileExistsError:
        pass
    return my_datadir


def get_token() -> str:
    """gets token from .api_token.txt file. If it doesn't exist,
    prompt for the user to paste it in.

    Returns:
        str: token text
    """
    token = ""
    token_file = get_my_datadir() / ".api_token.txt"
    if token_file.exists():
        with open(token_file, "r") as f:
            token = f.readline().rstrip()
    else:
        token = input("Paste your Joplin API Token:")
        with open(token_file, "w") as f:
            f.write(token.rstrip())
    return token


def get_token_suffix():
    return "?token=" + get_token()
