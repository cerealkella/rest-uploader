# -*- coding: utf-8 -*-

"""Main module. Launch by running python -m rest_uploader.cli"""

import os
import platform
import time
import base64
import mimetypes
import json
import requests
import csv
from tabulate import tabulate
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .img_process import (
    extract_text_from_image,
    extract_text_from_pdf,
    pdf_page_to_image,
    pdf_valid,
    TEMP_PATH,
)
from .api_token import get_token_suffix
from pathlib import Path


"""
2018-09-24 JRK
This program was created to upload files from a folder specified in the
PATH variable to Joplin. The following resource was helpful in figuring out
the logic for Watchdog:
https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes

Tested with the following extensions:
.md
.txt
.pdf
.png
.jpg
.url

Caveat
Uploader only triggered upon new file creation, not modification
"""


class MyHandler(FileSystemEventHandler):
    def _event_handler(self, path):
        filename, ext = os.path.splitext(path)
        if ext not in (".tmp", ".part", ".crdownload") and ext[:2] not in (".~"):
            for i in range(10):
                filesize = os.path.getsize(path)
                if filesize < 1 or (ext == ".pdf" and not pdf_valid(path)):
                    print("Incomplete file. Retrying...")
                    if i == 9:
                        print("timeout error, invalid file")
                        return False
                    time.sleep(5)
                elif filesize > 10000000:
                    print(f"Filesize = {filesize}. Too big for Joplin, skipping upload")
                    break
                else:
                    upload(path)
                    return True
        else:
            print("Detected temp file. Temp files are ignored.")

    def on_created(self, event):
        print(event.event_type + " -- " + event.src_path)
        self._event_handler(event.src_path)

    def on_moved(self, event):
        print(event.event_type + " -- " + event.dest_path)
        self._event_handler(event.dest_path)


# Set working Directory
def set_working_directory():
    if os.getcwd() != os.chdir(os.path.dirname(os.path.realpath(__file__))):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))


def set_token():
    global TOKEN
    TOKEN = get_token_suffix()


def set_autotag(autotag):
    global AUTOTAG
    AUTOTAG = True
    if autotag == "no":
        AUTOTAG = False


def set_endpoint(server, port):
    global ENDPOINT
    ENDPOINT = f"http://{server}:{port}"
    print(f"Endpoint: {ENDPOINT}")


def initialize_notebook(notebook_name):
    global NOTEBOOK_NAME
    NOTEBOOK_NAME = notebook_name
    global NOTEBOOK_ID
    NOTEBOOK_ID = ""
    return NOTEBOOK_NAME


def set_notebook_id(notebook_name=None):
    """ Find the ID of the destination folder 
    adapted logic from jhf2442 on Joplin forum
    https://discourse.joplin.cozic.net/t/import-txt-files/692
    """
    global NOTEBOOK_NAME
    global NOTEBOOK_ID
    if notebook_name is not None:
        NOTEBOOK_NAME = initialize_notebook(notebook_name)
    try:
        res = requests.get(ENDPOINT + "/folders" + TOKEN)
        folders = res.json()
        for folder in folders:
            if folder.get("title") == NOTEBOOK_NAME:
                NOTEBOOK_ID = folder.get("id")
        if NOTEBOOK_ID == "":
            for folder in folders:
                if "children" in folder:
                    for child in folder.get("children"):
                        if child.get("title") == NOTEBOOK_NAME:
                            NOTEBOOK_ID = child.get("id")
        return NOTEBOOK_ID
    except requests.ConnectionError as e:
        print("Connection Error - Is Joplin Running?")
        return "err"


def read_text_note(filename):
    with open(filename, "r") as myfile:
        text = myfile.read()
        print(text)
    return text


def read_csv(filename):
    return csv.DictReader(open(filename))


def apply_tags(text_to_match, note_id):
    """ Rudimentary Tag match using OCR'd text """
    res = requests.get(ENDPOINT + "/tags" + TOKEN)
    tags = res.json()
    counter = 0
    for tag in tags:
        if tag.get("title").lower() in text_to_match.lower():
            counter += 1
            tag_id = tag.get("id")
            response = requests.post(
                ENDPOINT + f"/tags/{tag_id}/notes" + TOKEN,
                data=f'{{"id": "{note_id}"}}',
            )
    print(f"Matched {counter} tag(s) for note {note_id}")
    return counter


def create_resource(filename):
    if NOTEBOOK_ID == "":
        set_notebook_id()
    basefile = os.path.basename(filename)
    title = os.path.splitext(basefile)[0]
    files = {
        "data": (json.dumps(filename), open(filename, "rb")),
        "props": (None, f'{{"title":"{title}", "filename":"{basefile}"}}'),
    }
    response = requests.post(ENDPOINT + "/resources" + TOKEN, files=files)
    print(response.json())
    return response.json()


def delete_resource(resource_id):
    apitext = ENDPOINT + "/resources/" + resource_id + TOKEN
    response = requests.delete(apitext)
    return response


def get_resource(resource_id):
    apitext = ENDPOINT + "/resources/" + resource_id + TOKEN
    response = requests.get(apitext)
    return response


def encode_image(filename, datatype):
    encoded = base64.b64encode(open(filename, "rb").read())
    img = f"data:{datatype};base64,{encoded.decode()}"
    return img


def set_json_string(title, NOTEBOOK_ID, body, img=None):
    if img is None:
        return '{{ "title": {}, "parent_id": "{}", "body": {} }}'.format(
            json.dumps(title), NOTEBOOK_ID, json.dumps(body)
        )
    else:
        return '{{ "title": "{}", "parent_id": "{}", "body": {}, "image_data_url": "{}" }}'.format(
            title, NOTEBOOK_ID, json.dumps(body), img
        )


def upload(filename):
    """ Get the default Notebook ID and process the passed in file"""
    basefile = os.path.basename(filename)
    title, ext = os.path.splitext(basefile)
    body = f"{basefile} uploaded from {platform.node()}\n"
    datatype = mimetypes.guess_type(filename)[0]
    if datatype is None:
        # avoid subscript exception if datatype is None
        if ext in (".url", ".lnk"):
            datatype = "text/plain"
        else:
            datatype = ""
    if datatype == "text/plain":
        body += read_text_note(filename)
        values = set_json_string(title, NOTEBOOK_ID, body)
    if datatype == "text/csv":
        table = read_csv(filename)
        body += tabulate(table, headers="keys", numalign="right", tablefmt="pipe")
        values = set_json_string(title, NOTEBOOK_ID, body)
    elif datatype[:5] == "image":
        img = encode_image(filename, datatype)
        body += "\n<!---\n"
        body += extract_text_from_image(filename)
        body += "\n-->\n"
        values = set_json_string(title, NOTEBOOK_ID, body, img)
    else:
        response = create_resource(filename)
        body += f"[{basefile}](:/{response['id']})"
        values = set_json_string(title, NOTEBOOK_ID, body)
        if response["file_extension"] == "pdf":
            # Special handling for PDFs
            body += "\n<!---\n"
            body += extract_text_from_pdf(filename)
            body += "\n-->\n"
            previewfile = f"{TEMP_PATH}\preview.png"
            if not os.path.exists(previewfile):
                previewfile = pdf_page_to_image(filename)
            img = encode_image(previewfile, "image/png")
            os.remove(previewfile)
            values = set_json_string(title, NOTEBOOK_ID, body, img)

    response = requests.post(ENDPOINT + "/notes" + TOKEN, data=values)
    # print(response)
    # print(response.text)
    if AUTOTAG:
        apply_tags(body, response.json().get("id"))
    print(f"Placed into note into notebook {NOTEBOOK_ID}: {NOTEBOOK_NAME}")
    return 0


def watcher(path=None):
    if path is None:
        path = str(Path.home())
    event_handler = MyHandler()
    print(f"Monitoring directory {path} for files")
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watcher()
