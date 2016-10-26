from .base_api import BaseAPI


class Rewards(BaseAPI):

    def available(self, merchant_id, store_id=None, user_email=None):
        url = self.client.base_url + "/rewards"

        # Generate items for the payload
        payload = {
            'token': self.client.token,
            'merchant': merchant_id,
        }

        if user_email:
            payload['user'] = user_email

        if store_id:
            payload['store_id'] = store_id

        return self.client._call('GET', url, payload)
