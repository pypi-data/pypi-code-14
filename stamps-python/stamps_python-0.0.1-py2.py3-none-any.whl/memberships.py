from .base_api import BaseAPI


class Memberships(BaseAPI):

    def status(self, merchant_id, user_identifier):
        url = self.client.base_url + "/memberships/status"

        payload = {
            'token': self.client.token,
            'merchant': merchant_id,
            'user': user_identifier
        }
        return self.client._call('GET', url, payload)

    def register(self, merchant_id, name, email, birthday, gender,
                 member_id=None, phone=None, address=None, password=None):

        url = self.client.base_url + "/memberships/register"
        payload = {
            'token': self.client.token,
            'merchant': merchant_id,
            'name': name,
            'email': email,
            'gender': gender,
            'birthday': birthday,
            'member_id': member_id,
            'phone': phone,
            'address': address,
            'password': password
        }
        return self.client._call('POST', url, payload)

    def add_stamps(self, merchant_id, email, stamps, note=''):
        url = self.client.base_url + "/memberships/add-stamps"
        payload = {
            'token': self.client.token,
            'merchant': merchant_id,
            'user': email,
            'note': note,
            'stamps': stamps
        }
        return self.client._call('POST', url, payload)
