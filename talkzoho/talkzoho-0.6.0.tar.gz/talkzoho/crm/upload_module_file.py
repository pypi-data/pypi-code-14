import os

import requests

from talkzoho.regions import US
from talkzoho.utils import create_url
from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN


def upload_file(module,
                *,
                auth_token=None,
                region=US,
                id,
                file_name,
                file_bytes):
    parameters   = {
        'id': int(id),
        'scope': SCOPE,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)}
    files = {
        'content': (file_name, file_bytes)}

    path     = API_PATH + '/' + module + '/uploadFile'
    endpoint = create_url(BASE_URL, tld=region, path=path)

    # TODO: replace with tornado client
    response = requests.post(endpoint, data=parameters, files=files)
    response.raise_for_status()

    return True
