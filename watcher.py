import sys
import os
import platform
import time
import base64
import magic
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from img_process import extract_text_from_image, extract_text_from_pdf,\
                        pdf_page_to_image, pdf_valid
from settings import PATH, SERVER, JOPLIN_NOTEBOOK
from api_token import get_token_suffix

'''
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

Caveat
Uploader only triggered upon new file creation, not modification
'''


TOKEN = get_token_suffix()


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event.event_type + " -- " + event.src_path)
        filename, ext = os.path.splitext(event.src_path)
        if ext not in ('.tmp', '.crdownload'):
            for i in range(10):
                if os.path.getsize(event.src_path) < 1 or (ext == '.pdf' and not pdf_valid(event.src_path)):
                    print("Incomplete file. Retrying...")
                    if i == 9:
                        print("timeout error, invalid file")
                        return False
                    time.sleep(5)
                else:
                    upload(event.src_path)
                    return True
        else:
            print("Detected temp file. Temp files are ignored.")


# Set working Directory
def set_working_directory():
    if os.getcwd() != os.chdir(os.path.dirname(os.path.realpath(__file__))):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))


def read_text_note(filename):
    with open(filename, 'r') as myfile:
        text = myfile.read()
        print(text)
    return text


def get_notebook_id():
    # Find the ID of the destination folder
    # adapted logic from jhf2442 on Joplin forum
    # https://discourse.joplin.cozic.net/t/import-txt-files/692
    res = requests.get(SERVER + "/folders" + TOKEN)
    folders = res.json()

    notebook_id = 0
    for folder in folders:
        if folder.get('title') == JOPLIN_NOTEBOOK:
            notebook_id = folder.get('id')
    if notebook_id == 0:
        for folder in folders:
            if 'children' in folder:
                for child in folder.get('children'):
                    if child.get('title') == JOPLIN_NOTEBOOK:
                        notebook_id = child.get('id')
    return notebook_id


def create_resource(filename):
    basefile = os.path.basename(filename)
    title = os.path.splitext(basefile)[0]
    files = {
        'data': (json.dumps(filename), open(filename, 'rb')),
        'props': (None, '{{"title":"{}", "filename":"{}"}}'.format(title,
                                                                   basefile))
    }
    response = requests.post(SERVER + '/resources' + TOKEN, files=files)
    print(response.json())
    return response.json()


def delete_resource(resource_id):
    apitext = SERVER + '/resources/' + resource_id + TOKEN
    response = requests.delete(apitext)
    return response


def get_resource(resource_id):
    apitext = SERVER + '/resources/' + resource_id + TOKEN
    response = requests.get(apitext)
    return response


def encode_image(filename, datatype):
    encoded = base64.b64encode(open(filename, "rb").read())
    img = "data:{};base64,{}".format(datatype, encoded.decode())
    return img


def set_json_string(title, notebook_id, body, img=None):
    if img is None:
        return '{{ "title": {}, "parent_id": "{}", "body": {} }}'\
            .format(json.dumps(title), notebook_id, json.dumps(body))
    else:
        return '{{ "title": "{}", "parent_id": "{}", "body": {}, "image_data_url": "{}" }}'\
            .format(title, notebook_id, json.dumps(body), img)


def upload(filename):
    basefile = os.path.basename(filename)
    title = os.path.splitext(basefile)[0]
    body = basefile + " uploaded from " + platform.node() + "\n"
    mime = magic.Magic(mime=True)
    datatype = mime.from_file(filename)
    notebook_id = get_notebook_id()
    if datatype == "text/plain":
        body += read_text_note(filename)
        values = set_json_string(title, notebook_id, body)
    elif datatype[:5] == "image":
        img = encode_image(filename, datatype)
        body += extract_text_from_image(filename)
        values = set_json_string(title, notebook_id, body, img)
    else:
        response = create_resource(filename)
        body += '[](:/{})'.format(response['id'])
        values = set_json_string(title, notebook_id, body)
        if response['file_extension'] == 'pdf':
            # Special handling for PDFs
            body += extract_text_from_pdf(filename)
            previewfile = pdf_page_to_image(filename)
            img = encode_image(previewfile, "image/png")
            print(len(body))
            if len(body) <= 100:
                # if embedded PDF text is minimal or does not exist,
                # run OCR the preview file
                body += extract_text_from_image(previewfile)
            values = set_json_string(title, notebook_id, body, img)

    response = requests.post(SERVER + '/notes' + TOKEN, data=values)
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
