import requests
import urllib3

urllib3.disable_warnings()

try:
    response = requests.request(
        'get', 'https://res-trans-app01/users',
        headers={'User-Id': 'e7074aa9'}, verify=False)
except requests.exceptions.SSLError, e:
   raise OSError('general SSL error, is the server certificate installed?')
