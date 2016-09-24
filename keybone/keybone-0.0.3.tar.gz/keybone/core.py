#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import gnupg
import logging


from plant import Node
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

from keybone import conf
from keybone.util import GPGSerializer

node = Node(__file__).dir
logger = logging.getLogger('keybone')

uid_regex = re.compile(r'(?P<name>.*?)\s*[(](?P<metadata>[^)]+)[)]\s*[<]\s*(?P<email>[^>]+)\s*[>]\s*')


class KeyAlreadyExists(Exception):
    def __init__(self, key):
        super(KeyAlreadyExists, self).__init__(key['email'])
        self.key = key


class InvalidKeyError(Exception):
    pass


class InvalidRecipient(Exception):
    pass


class SymmetricalHelper(object):
    def __init__(self, key):
        if not key:
            self.symmetric = None
        else:
            self.symmetric = Fernet(key)

    def encrypt(self, data):
        if self.symmetric:
            return self.symmetric.encrypt(data)
        logger.warning('the "fernet_key" setting is not available. The data will not be encrypted')
        return data

    def decrypt(self, cipher_text):
        if not self.symmetric:
            return cipher_text

        try:
            return self.symmetric.decrypt(bytes(cipher_text))
        except InvalidToken:
            return cipher_text


def ensure_secure_key_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    stat = os.stat(path)
    mode = oct(stat.st_mode)[-3:]
    if mode != '700':
        # side-effect: set files to 0700 mode
        logging.warning('changing mode of {0} to 0700'.format(os.path.abspath(path)))
        os.chmod(path, 0700)

    return path


class KeyBone(object):
    def __init__(self, path=conf.key_home, password=conf.fernet_key):
        self.key_home = ensure_secure_key_folder(path)  # this has a side-effect in the file-system
        self.symmetric = SymmetricalHelper(password)
        self.gpg = gnupg.GPG(gnupghome=path)
        self.serialize = GPGSerializer(self)

    def sort_keys(self, keys):
        ordered = sorted(sorted(keys, key=lambda x: x['email']), key=lambda x: x['private'], reverse=True)
        uniq = []
        final = []
        for key in ordered:
            keyid = key['keyid']

            if keyid in uniq:
                continue

            uniq.append(keyid)
            final.append(key)

        return final

    def list_private_keys(self):
        return self.sort_keys(map(self.serialize.key, self.gpg.list_keys(True)))

    def list_public_keys(self):
        return self.sort_keys(map(self.serialize.key, self.gpg.list_keys(False)))

    def list_keys(self):
        all_keys = []
        all_keys.extend(self.list_private_keys())
        all_keys.extend(self.list_public_keys())
        return self.sort_keys(all_keys)

    def generate_key(self, name, email, passphrase, expire_date=0):
        for key in self.list_keys():
            if email in key['email']:
                raise KeyAlreadyExists(key)

        key_input = self.gpg.gen_key_input(**{
            "key_type": "RSA",
            "key_length": 2048,

            # # revogation ?
            # "subkey_type": "RSA",
            # "subkey_length": 2048,

            "name_real": name,
            "name_comment": self.symmetric.encrypt(json.dumps({
                'email': email,
                'name': name,
            })),
            "name_email": email,
            "passphrase": passphrase,
            "expire_date": expire_date,
        })
        return self.gpg.gen_key(key_input)

    def import_key(self, key):
        result = self.gpg.import_keys(key)
        if not result:
            msg = 'Invalid GPG key: {0}'.format(key)
            raise InvalidKeyError(msg)

        return result

    def get_key_for_id(self, keyid):
        for key in self.list_keys():
            if key['keyid'] == keyid:
                return key

    def get_key_for_fingerprint(self, fingerprint):
        for key in self.list_keys():
            if key['fingerprint'] == fingerprint:
                return key

    def get_key_for_email(self, email):
        for key in self.list_keys():
            if key['email'] == email:
                return key

    def get_key(self, id_fingerprint_or_email):
        return (
            self.get_key_for_fingerprint(id_fingerprint_or_email) or
            self.get_key_for_id(id_fingerprint_or_email) or
            self.get_key_for_email(id_fingerprint_or_email)
        ) or {
            'keyid': None,
            'fingerprint': None,
            'email': None,
            'passphrase': None,
        }

    def get_fingerprint(self, recipient):
        key = self.get_key(recipient)
        return key['fingerprint']

    def get_keyid(self, recipient):
        key = self.get_key(recipient)
        return key['keyid']

    def get_passphrase(self, recipient):
        key = self.get_key(recipient)
        return key.get('passphrase')

    def encrypt(self, recipient, plaintext, should_sign=False):
        fingerprint = self.get_fingerprint(recipient)
        if not fingerprint:
            msg = 'there are no keys for the recipient for email: {0}'.format(recipient)
            raise InvalidRecipient(msg)

        kw = {}
        passphrase = self.get_passphrase(recipient)

        if passphrase:
            kw['passphrase'] = passphrase

        if should_sign:
            kw['sign'] = fingerprint

        crypt = self.gpg.encrypt(plaintext.strip(), recipient, always_trust=True, **kw)
        if crypt.data:
            return crypt.data

        logger.error(" - ".join([crypt.status, crypt.stderr]))

    def decrypt(self, ciphertext, passphrase=None):
        crypt = self.gpg.decrypt(ciphertext.strip(), passphrase=passphrase, always_trust=True)
        if crypt.data:
            return crypt.data

        elif passphrase:
            logger.error(" - ".join([crypt.status, crypt.stderr]))
            return

        uid = self.serialize.extract_uid([crypt.stderr])
        if not uid:
            logger.error(crypt.stderr)
            return

        # TODO: check for the right key by fingerprint, emails are NOT
        # unique in a keyring
        key = self.get_key(uid['email'])
        if not key['private']:
            raise InvalidKeyError('cannot decrypt because private key is missing for: {0}'.format(uid['email']))

        passphrase = uid.get('passphrase')
        return self.decrypt(ciphertext, passphrase)

    def sign(self, recipient, data):
        keyid = self.get_keyid(recipient)
        passphrase = self.get_passphrase(recipient)
        crypt = self.gpg.sign(data, keyid=keyid, passphrase=passphrase)
        if not crypt.data:
            logger.error(crypt.stderr)
            return

        return crypt.data

    def verify(self, data):
        crypt = self.gpg.verify(data)
        if not crypt.status:
            logger.error(crypt.stderr)
            return

        return crypt.status, crypt.trust_text
