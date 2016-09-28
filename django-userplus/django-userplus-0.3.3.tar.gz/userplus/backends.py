from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from facebook import GraphAPI


class UserPlusBackend(ModelBackend):

    def authenticate(self, username=None, password=None, email=None, facebook_token=None, **kwargs):
        if facebook_token and getattr(settings, 'USERPLUS_ENABLE_FACEBOOK_LOGIN', None):
            user = self.authenticate_facebook(facebook_token)

        elif email:
            UserModel = get_user_model()
            try:
                user = UserModel._default_manager.get(email=email.lower())
                if not user.check_password(password):
                    user = None
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                UserModel().set_password(password)
                return
        else:
            user = super(UserPlusBackend, self).authenticate(
                username=username.lower(), password=password, **kwargs)

        if getattr(user, 'is_active', None):
            return user

    def authenticate_facebook(self, token):
        data = GraphAPI(token).get_object('me', fields='email,name')
        email = data.get('email')
        if email:
            UserModel = get_user_model()
            try:
                user = UserModel._default_manager.get(email=email.lower())
            except UserModel.DoesNotExist:
                username = data.get('name').replace(' ', '').lower()
                if UserModel.objects.filter(username=username).exists():
                    username = ''.join([username, data.get('id')])

                counter = 0
                while UserModel.objects.filter(username=username).exists():
                    counter += 1
                    username = username + str(counter)
                user = UserModel.objects.create_user(username, email=email, is_facebook_user=True)
            return user
        return None
