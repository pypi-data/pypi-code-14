from .signals import unrestrict_user


class OpenCredValidator(object):
    def password_changed(self, password, user=None, password_validators=None):
        unrestrict_user(user)
