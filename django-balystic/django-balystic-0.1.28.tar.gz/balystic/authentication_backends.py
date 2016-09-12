from django.contrib.auth import get_user_model
from balystic.client import Client


class BalysticBackend(object):
    """
    Sends the credentials to balystic for authentication
    and allows the user to log in depending on the outcome
    of the operation.
    """
    user_model = get_user_model()

    def authenticate(self, email, password):
        client = Client()
        response = client.authenticate_user(email=email, password=password)
        if 'user' in response.keys():
            try:
                user = self.user_model.objects.get(username=response['user']['username'])
                user.generics = response['user']['generics']
                user.save()
            except self.user_model.DoesNotExist:
                user = self.user_model(email=email, username=response['user']['username'], generics=response['user']['generics'])
                user.save()
            user.url = response['url']
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return self.user_model.objects.get(pk=user_id)
        except self.user_model.DoesNotExist:
            return None
