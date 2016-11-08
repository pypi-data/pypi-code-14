'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

import codecs
import hashlib
import os

import bcrypt

from sxclient.tools import toutf8, tobytes
from sxclient.exceptions import InvalidUserKeyError
from sxclient.defaults import (
    VALID_DECODED_KEY_LENGTH,
    VALID_ENCODED_KEY_LENGTH,
    VALID_ENCODED_KEY_CHARACTERS,
)

__all__ = ['UserData']


class UserData(object):
    '''
    Prepare user access data.

    In addition to the default initialization, the following class methods can
    be used to initialize the object:
      - from_key;
      - from_key_path;
      - from_userpass_pair.

    For example, to initialize the object based on username and password, run:
        UserData.from_userpass_pair(username, password, uuid)
    '''

    def __init__(self, dec_key):
        # type: (bytes) -> None
        if len(dec_key) != VALID_DECODED_KEY_LENGTH:
            raise InvalidUserKeyError('Invalid decoded user key length')
        self._key = dec_key

    @property
    def key(self):
        # type: () -> bytes
        return self._key

    @property
    def uid(self):
        # type: () -> bytes
        return self._key[:20]

    @property
    def secret_key(self):
        # type: () -> bytes
        return self._key[20:40]

    @property
    def padding(self):
        # type: () -> bytes
        return self._key[40:42]

    @classmethod
    def from_key(cls, enc_key):
        # type: (str) -> UserData
        '''Prepare user access data using base64-encoded user key.'''
        dec_key = cls._decode_key(enc_key)
        return cls(dec_key)

    @classmethod
    def from_key_path(cls, key_path):
        # type: (str) -> UserData
        '''
        Prepare user access data using path to the file containing
        base64-encoded user key.
        '''
        key_path = os.path.expanduser(key_path)
        enc_key = cls._load_key(key_path)
        dec_key = cls._decode_key(enc_key)
        return cls(dec_key)

    @classmethod
    def from_userpass_pair(cls, username, password, cluster_uuid):
        # type: (str, str, str) -> UserData
        '''
        Prepare user access data based on username, password and cluster UUID.

        Note that username and password should be encoded in UTF-8.
        '''
        username_bytes = tobytes(username)  # type: bytes
        password_bytes = tobytes(password)  # type: bytes
        cluster_uuid_bytes = tobytes(cluster_uuid)  # type: bytes

        # prepare uid
        sha1 = hashlib.sha1()
        sha1.update(username_bytes)
        uid = sha1.digest()

        # prepare salt for password hashing
        sha1 = hashlib.sha1()
        sha1.update(cluster_uuid_bytes)
        sha1.update(username_bytes)
        salt = sha1.digest()[:16]
        encsalt = bcrypt.encode_salt(salt, 12)

        # prepare hashed password with '2b' prefix
        hashpw = tobytes(bcrypt.hashpw(password_bytes, encsalt))
        hashpw = b'$2b' + hashpw[3:]

        # prepare secret key
        sha1 = hashlib.sha1()
        sha1.update(cluster_uuid_bytes)
        sha1.update(hashpw)
        secret = sha1.digest()

        dec_key = b''.join([uid, secret, b'\x00\x00'])
        return cls(dec_key)

    @staticmethod
    def _load_key(path):
        # type: (str) -> str
        '''Read base64-encoded key from 'path'.'''
        with open(path, 'rb') as keyfile:
            enc_key = keyfile.read(VALID_ENCODED_KEY_LENGTH)
        return enc_key

    @staticmethod
    def _decode_key(enc_key):
        # type: (str) -> bytes
        '''Verify and decode base64-encoded key.'''
        if len(enc_key) != VALID_ENCODED_KEY_LENGTH:
            raise InvalidUserKeyError('Invalid base64-encoded user key length')

        # Python 2.7.10 documentation incorrectly states that
        # 'base64.b64decode' raises 'TypeError' in case of invalid input
        # characters. In reality, invalid input characters are silently
        # ignored. The issue has been reported in
        #   https://bugs.python.org/issue22088
        # Input validity is checked independently of 'base64.b64decode', below.
        for char in toutf8(enc_key):
            if char not in VALID_ENCODED_KEY_CHARACTERS:
                raise InvalidUserKeyError(
                    "Invalid character in base64-encoded user key"
                )

        dec_key = codecs.decode(tobytes(enc_key), 'base64')
        return dec_key  # type: ignore FIXME
