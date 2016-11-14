import requests

from .config import API_ROOT


DIFFICULTIES = {
    'e': 1,
    'n': 2,
    'x': 3,
}

def create_challenge(api_key, **fields):
    headers = {
        'apiKey': api_key,
    }
    url = '%schallenge' % API_ROOT
    response = requests.post(url, headers=headers, json=fields)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception('Could not create challenge: %s' % response.json()['message'])


def get_challenge(challenge_id):
    if not challenge_id:
        return None
    try:
        r = requests.get('%schallenge/%d' % (API_ROOT, challenge_id))
        return r.json()
    except Exception:
        return None


def upload_tasks(api_key, challenge_id, tasks):
    url = '%schallenge/%s/tasks' % (API_ROOT, challenge_id)
    headers = {
        'apiKey': api_key,
    }
    response = requests.post(url, headers=headers, json=tasks)
    return response
