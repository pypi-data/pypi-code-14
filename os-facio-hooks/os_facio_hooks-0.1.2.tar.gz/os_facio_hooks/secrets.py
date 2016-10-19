import hashlib
import uuid
from facio.state import state

def run():
    password = str(uuid.uuid1())
    password_sha256_hash = get_password_hash(password)
    secret_key = str(uuid.uuid1())
    state.update_context_variables({'SECRET_KEY': secret_key})
    state.update_context_variables({'JWT_PASSWORD': password})
    state.update_context_variables({'SHA256_PASSWORD': password_sha256_hash})
    # print('password: ' + password)
    # print('password_sha256_hash: ' + password_sha256_hash)
    # print('secret_key: ' + secret_key)


def get_password_hash(password):
    password_to_hash = str(password)
    password_to_hash_bytes = bytes(password_to_hash, 'utf-8')
    hash_object = hashlib.sha256(password_to_hash_bytes)
    hex_result = hash_object.hexdigest()
    return hex_result