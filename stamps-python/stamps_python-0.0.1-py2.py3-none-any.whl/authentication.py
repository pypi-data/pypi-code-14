from .base_api import BaseAPI


class Authentication(BaseAPI):

    def login(self, email, password):
        url = self.client.base_url + "/auth/login"
        payload = {
            'token': self.client.token,
            'username': email,
            'password': password
        }
        return self.client._call('POST', url, payload)
