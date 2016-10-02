import time

from Crypto.Random import random
import requests


class Client:
    RequestFailed = type('RequestFailed', (Exception,), {})
    InvalidSignature = type('InvalidSignature', (RequestFailed,), {})

    class dto_class(dict):
        def __getattr__(self, name):
            if name not in self:
                raise AttributeError(name)
            return self[name]

    def __init__(self, host, base_url='/', scheme="http"):
        self.host = host
        self.base_url = base_url
        self.scheme = scheme

    def verify_signature(self, signature, phonenumber, token):
        """Verify the signature of the phonenumber and token at the
        remote host.
        """
        url = self._make_url('/phonenumbers/token')
        params = {
            'signature': signature,
            'token': token,
            'phonenumber': phonenumber
        }
        response = requests.post(url, json=params)
        if response.status_code == 403:
            raise self.InvalidSignature(signature, phonenumber, token)

    def request_confirmation(self, display_name, phonenumber, template, expires=None):
        """Send a request to verify to the given `phonenumber`.

        Args:
            display_name: the name to be displayed to the user; max
                of 11 character.
            phonenumber: a valid ITU-T E.164 phonenumber.
            template: a message template containing a ``{token}``
                variable. No more than 64 characters.
            expires: an optional unsigned long integer specifying when
                the request expires, in milliseconds from now.
        """
        url = self._make_url('/phonenumbers/confirm/')
        if "{token}" not in template:
            raise ValueError("template string must contain {token}")

        if len(display_name) > 11:
            raise ValueError("display_name may be at most 11 characters.")

        token = random.randint(100000, 999999)
        params = {
            'message': template.format(token=token),
            'token': str(token),
            'phonenumber': phonenumber,
            'display_name': display_name,
        }
        if expires is not None:
            params['expires'] = int(time.time() * 1000) + expires

        response = requests.post(url, json=params)
        if response.status_code >= 400:
            raise self.RequestFailed(url, response.status_code, response.get_data())

        return self.dto_class(**response.json())

    def _make_url(self, path):
        return "%s://%s%s/%s" % (self.scheme, self.host,
            self.base_url, path.lstrip('/'))
