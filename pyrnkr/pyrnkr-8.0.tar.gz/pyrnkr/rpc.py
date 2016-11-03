import requests


def call(mnemonic, payload, async=True):
    command = {
        'payload': payload,
        'async': async
    }

    endpoint = 'https://dev.rnkr.io/rpc/{0}/execute'.format(mnemonic)
    result = requests.post(endpoint, json=command)
    if result.status_code != 200:
        return None, 'could not execute artifact: {0}'.format(result.text)

    return result.json()
