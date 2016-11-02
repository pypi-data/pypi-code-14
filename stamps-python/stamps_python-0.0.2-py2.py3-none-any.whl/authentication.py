from .base_api import BaseAPI


class Authentication(BaseAPI):

    def login(self, email=None, password=None):
        url = self.client.base_url + "/auth/login"
        payload = {
            'token': self.client.token,
            'username': email,
            'password': password
        }
        return self.client._call('POST', url, payload)
