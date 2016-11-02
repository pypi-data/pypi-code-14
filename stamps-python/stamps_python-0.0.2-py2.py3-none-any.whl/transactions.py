from .base_api import BaseAPI


class Transactions(BaseAPI):

    def add(self, user=None, total_value=None,
            invoice_number=None, created=None, items=None):
        url = self.client.base_url + "/transactions/add"

        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'store': self.client.store_id,
            'user': user,
            'invoice_number': invoice_number,
            'total_value': total_value,
            'created': created,
        }

        if items:
            payload["items"] = items

        return self.client._call('POST', url, payload)
