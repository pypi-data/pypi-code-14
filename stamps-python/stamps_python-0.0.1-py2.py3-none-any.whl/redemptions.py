from .base_api import BaseAPI


class Redemptions(BaseAPI):

    def add(self, merchant_id, store_id,
            user_email, reward_id, redeem_type):
        url = self.client.base_url + "/redemptions/add"

        payload = {
            'token': self.client.token,
            'merchant': merchant_id,
            'user': user_email,
            'store': store_id,
            'reward': reward_id,
            'type': redeem_type,
        }

        return self.client._call('POST', url, payload)

    def cancel(self, redemption_id):
        url = self.client.base_url + "/redemptions/cancel"

        payload = {
            'token': self.client.token,
            'id': redemption_id
        }
        return self.client._call('POST', url, payload)
