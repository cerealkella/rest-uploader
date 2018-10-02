import os
import requests
from json import dumps
from api_token import get_token_suffix
from settings import SERVER, PATH


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


'''
resp = (create_resource(PATH + "test.pdf"))
print(resp)
print(resp['id'])
print(get_resource(resp['id']))
print(delete_resource(resp['id']))
print(get_resource(resp['id']))
'''
