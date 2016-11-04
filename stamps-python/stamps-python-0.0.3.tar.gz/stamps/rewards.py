from .base_api import BaseAPI


class Rewards(BaseAPI):

    def available(self, user=None, **kwargs):
        url = self.client.base_url + "/rewards"

        # Generate items for the payload
        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
        }

        if user:
            payload['user'] = user

        if self.client.store_id:
            payload['store_id'] = self.client.store_id

        payload.update(kwargs)
        return self.client._call('GET', url, payload)
