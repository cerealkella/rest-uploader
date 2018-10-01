import sys
import os
import platform
import time
import base64
import magic
import json
from requests import post
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from img_process import extract_text_from_image

'''
2018-09-24 JRK
This program was created to upload files from a folder specified in the
PATH variable to Joplin. The following resource was helpful in figuring out
the logic for Watchdog:
https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes

The Joplin Webclipper API seems to only support image file uploads,
Unfortunately, PDFs do not work.
Plain text files work -- tested with .md and .txt extensions.

Caveat
Uploader only triggered upon new file creation, not modification
'''


SERVER = 'http://127.0.0.1:41184/notes'
PATH = './upload/'


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event.event_type + " -- " + event.src_path)
        upload(event.src_path)


# Set working Directory
def set_working_directory():
    if os.getcwd() != os.chdir(os.path.dirname(os.path.realpath(__file__))):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))


def read_text_note(filename):
    with open(filename, 'r') as myfile:
        text = myfile.read()
        print(text)
    return text


def upload(filename):
    mime = magic.Magic(mime=True)
    datatype = mime.from_file(filename)
    encoded = base64.b64encode(open(filename, "rb").read())
    img = "data:{};base64,{}".format(datatype, encoded.decode())
    title = os.path.basename(filename)
    if datatype == "text/plain":
        # this is not working correctly yet
        # will bomb if there are quotes in the text file
        body = read_text_note(filename)
        print(body)
        values = '{{ "title": "{}", "body": {} }}'\
            .format(title, json.dumps(body))
        print(values)
        print(repr(values))
    else:
        body = filename + " uploaded from " + platform.node()
        body += "\n"
        body += extract_text_from_image(filename)
        values = '{{ "title": "{}", "body": {}, "image_data_url": "{}" }}'\
            .format(title, json.dumps(body), img)
    response = post(SERVER, data=values)
    print(response)
    print(response.text)
    print(response.json())


if __name__ == "__main__":
    set_working_directory()
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
