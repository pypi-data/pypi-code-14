import base64
from hashlib import sha1
import hmac
import six


class Signature(object):
    def __init__(self, key):
        self.key = key.encode('utf-8')

    def validate(self, signature, data):
        return signature == self.generate(data)

    def generate(self, s):
        self.generate_with_key(s, self.key)

    @classmethod
    def validate_with_key(cls, signature, data, key):
        return signature == cls.generate_with_key(data, key)

    @classmethod
    def generate_with_key(cls, s, key):
        return six.text_type(base64.urlsafe_b64encode(
            hmac.new(key.encode('utf-8'), six.text_type(s).encode('utf-8'), sha1).digest()
        ), 'ascii').strip('=')
