from _sha256 import sha256
import time

from itsdangerous import Signer


class ApiKeySigner(Signer):
    def __init__(self, secret_key):
        super(ApiKeySigner, self).__init__(secret_key, digest_method=sha256, key_derivation='none')

    def sign(self, value):
        if type(value) is str:
            value = value.encode()
        return super(ApiKeySigner, self).sign(value)


class BitcoinaverageBaseClient:
    def __init__(self, secret_key, public_key):
        self.secret_key = secret_key
        self.public_key = public_key

        self.signer = ApiKeySigner(secret_key)

    @property
    def signature_header(self):
        return self.signer.sign('{}.{}'.format(int(time.time()), self.public_key))
