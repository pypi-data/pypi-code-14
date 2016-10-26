from .base_api import BaseAPI


class Transactions(BaseAPI):

    def add(self, merchant_id, store_id, user_email,
            total_value, invoice_number, created=None,
            items=None):
        url = self.client.base_url + "/transactions/add"

        payload = {
            'token': self.client.token,
            'merchant': merchant_id,
            'user': user_email,
            'store': store_id,
            'invoice_number': invoice_number,
            'total_value': total_value,
            'created': created,
        }

        if items:
            payload["items"] = items

        return self.client._call('POST', url, payload)
