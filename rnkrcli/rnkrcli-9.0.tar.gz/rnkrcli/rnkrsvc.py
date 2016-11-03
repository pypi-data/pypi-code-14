import requests


def __make_request(endpoint, payload, token, expected=200, method='post'):
    headers = {
        'Authorization': 'Token {0}'.format(token),
        'Content-Type': 'application/json',
    }

    if method == 'post':
        res = requests.post(
            endpoint,
            json=payload if payload else None,
            headers=headers
        )

    elif method == 'get':
        res = requests.get(
            endpoint,
            headers=headers
        )

    if res.status_code != expected:
        raise Exception('failed to execute request: ' + res.text)

    return res.json()


def get_artifact(pk, token):
    return __make_request(
        'https://dev.rnkr.io/artifacts/{:d}'.format(pk),
        payload=None,
        token=token,
        method='get'
    )


def run_artifact(mnemonic, payload, token, async=False):
    command = {
        'async': async,
        'payload': payload
    }

    return __make_request(
        'https://dev.rnkr.io/rpc/{0}/execute'.format(mnemonic),
        command,
        token
    )


def create_artifact(payload, token):
    return __make_request(
        'https://dev.rnkr.io/artifacts/',
        payload,
        token,
        expected=201
    )
