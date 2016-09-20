"""
Codecs used for keys, etc.
"""
import json
import zlib
import base64
import rsa
import pyaes
import os
import hashlib
from django.conf import settings


def encrypt(rsa_key, data):
    "Encrypt/Encode data dictionary using json, utf8, zlib, aes and rsa."
    data_json = json.dumps(data)
    data_utf8 = data_json.encode('utf8')
    data_zlib = zlib.compress(data_utf8, 9)
    key_aes = os.urandom(32)
    aes = pyaes.AESModeOfOperationCTR(key_aes)
    data_aes = aes.encrypt(data_zlib)
    rsa_aes = rsa.encrypt(key_aes, rsa_key)
    returns = rsa_aes+data_aes
    return returns

def decrypt(rsa_key, encrypted):
    "Decrypt/Decode to data dictionary using rsa, aes, zlib, utf8 and json."
    size = settings.RSA_KEYSIZE // 8
    rsa_aes = encrypted[:size]
    encrypted = encrypted[size:]
    key_aes = rsa.decrypt(rsa_aes, rsa_key)
    aes = pyaes.AESModeOfOperationCTR(key_aes)
    data_aes = aes.decrypt(encrypted)
    data_zlib = zlib.decompress(data_aes)
    data_utf8 = data_zlib.decode('utf8')
    data = json.loads(data_utf8)
    return data

def encode_key(decrypt_key, url):
    "Encode key and url to hexdigest and environment variable."
    tmp = dict()
    tmp['u'] = url
    tmp['n'] = decrypt_key.n
    tmp['e'] = decrypt_key.e
    tmp['d'] = decrypt_key.d
    tmp['p'] = decrypt_key.p
    tmp['q'] = decrypt_key.q

    tmp_json = json.dumps(tmp)
    tmp_utf8 = tmp_json.encode('utf8')
    tmp_zlib = zlib.compress(tmp_utf8, 9)
    tmp_b64e = base64.b64encode(tmp_zlib)
    tmp_envk = tmp_b64e.decode('utf8')
    n_bytes = decrypt_key.n.to_bytes(settings.RSA_KEYSIZE // 8, 'big')
    digest = hashlib.sha224(n_bytes).hexdigest().upper()
    return digest, tmp_envk

def decode_key(encoded):
    "Decode environment variable to url and key."
    tmp_byte = encoded.encode('utf8')
    tmp_b64e = base64.b64decode(tmp_byte)
    tmp_zlib = zlib.decompress(tmp_b64e)
    tmp_utf8 = tmp_zlib.decode('utf8')
    tmp = json.loads(tmp_utf8)
    key = rsa.PrivateKey(tmp['n'], tmp['e'], tmp['d'], tmp['p'], tmp['q'])
    return tmp['u'], key
