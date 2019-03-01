import os
import requests
from json import dumps
from api_token import get_token_suffix
from settings import SERVER, PATH, JOPLIN_NOTEBOOK
from watcher import get_notebook_id

TOKEN = get_token_suffix()


def create_resource(filename):
    basefile = os.path.basename(filename)
    title = os.path.splitext(basefile)[0]
    files = {
        'data': (dumps(filename), open(filename, 'rb')),
        'props': (None, '{{"title":"{}", "filename":"{}"}}'.format(title,
                                                                   basefile))
    }
    response = requests.post(SERVER + '/resources' + TOKEN, files=files)
    return response.json()


def delete_resource(resource_id):
    apitext = SERVER + '/resources/' + resource_id + TOKEN
    response = requests.delete(apitext)
    return response


def get_resource(resource_id):
    apitext = SERVER + '/resources/' + resource_id + TOKEN
    response = requests.get(apitext)
    return response


def get_folders():
    req = requests.get(SERVER + "/folders" + TOKEN)
    print(SERVER)
    return req.json()


def get_tags():
    req = requests.get(SERVER + "/tags" + TOKEN)
    print(SERVER)
    return req.json()


'''
resp = (create_resource(PATH + "test.pdf"))
print(resp)
print(resp['id'])
print(get_resource(resp['id']))
print(delete_resource(resp['id']))
print(get_resource(resp['id']))
'''

SERVER = 'http://localhost:41184'

# print(get_notebook_id())
# print(get_folders())
import base64

def write_encoded():
    encoded = base64.b64encode(open("mcconn.png", "rb").read())
    print(type(encoded))
    # img = "data:{};base64,{}".format(datatype, encoded.decode())
    with open('encodedimg.txt', 'w') as f:
        f.write(encoded.decode("utf-8"))

# write_encoded()

print(get_tags())