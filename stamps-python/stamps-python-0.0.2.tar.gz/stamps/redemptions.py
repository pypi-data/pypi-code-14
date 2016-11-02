from .base_api import BaseAPI


class Redemptions(BaseAPI):

    def add(self, user=None, id=None, type=None):
        url = self.client.base_url + "/redemptions/add"

        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'store': self.store_id,
            'user': user,
            'reward': id,
            'type': type,
        }

        return self.client._call('POST', url, payload)

    def cancel(self, id=None):
        url = self.client.base_url + "/redemptions/cancel"

        payload = {
            'token': self.client.token,
            'id': id
        }
        return self.client._call('POST', url, payload)
