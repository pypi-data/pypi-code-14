from django.contrib.auth.tokens import PasswordResetTokenGenerator as DjangoPasswordResetTokenGenerator


class PasswordResetTokenGenerator(DjangoPasswordResetTokenGenerator):
    key_salt = 'fEqUvMDIIY1Yh70GbH9u7e8Fyv716xSs' # IN SETTINGS

password_reset_token_henerator = PasswordResetTokenGenerator()


class AccountActivationTokenGenerator(DjangoPasswordResetTokenGenerator):
    key_salt = 'fEqUvMDIIY1Yh10GbH9u7e8Fyv716xSs'

account_activation_token = AccountActivationTokenGenerator()
