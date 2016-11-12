import hashlib
from functools import wraps
from flask import current_app
from flask_jwt import JWTError
from datetime import datetime
from werkzeug.security import safe_str_cmp
from commons.persistence import (
    get, get_related, get_all_related
)


def hash_pwd(pwd, hash_algo, *salt):
    hash_fn = getattr(hashlib, hash_algo)()

    [hash_fn.update(i.encode()) for i in salt]
    hash_fn.update(pwd.encode())

    return hash_fn.hexdigest()


def authenticate(user_email, user_passwd):
    node = get("User", "email", user_email)
    salt = get_related(node, "WITH_SALT")

    authenticated = (
        salt is not None and safe_str_cmp(
            hash_pwd(user_passwd, salt['algo'], salt['salt']),
            node['passwd']
        )
    )

    return authenticated and node or None


def payload_handler(node):
    iat = datetime.utcnow()
    data = {
        "iat": iat,
        "exp": iat + current_app.config.get('JWT_EXPIRATION_DELTA'),
        "nbf": iat + current_app.config.get('JWT_NOT_BEFORE_DELTA'),
        "uid": node['uid'],
        "scopes": []
    }

    related = get_all_related(node, "OF_PLAYER")

    add_scope = data["scopes"].append
    add_attribute = data.__setitem__

    for k in related:
        add_scope(k["kind"])
        add_attribute(k["kind"], k["uid"])

    for scope in get_all_related(node, "WITH_SCOPE"):
        add_scope(scope["scope"])

    if not data['scopes']:
        data['scopes'] = ['rougue']

    return data


def jwt_scope_any_of(scopes, realm=None):
    from flask_jwt import _jwt_required

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(realm)
            if not (scopes & set(get_scoped_info('scopes'))):
                raise JWTError(
                    "Scope Missing", "Missing required scope for resource"
                )
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def jwt_scope_all_of(scopes, realm=None):
    from flask_jwt import _jwt_required

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(realm)
            if not (scopes & set(get_scoped_info('scopes')) == scopes):
                raise JWTError(
                    "Scope Missing", "Missing required scopes for resource"
                )
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def refresh_scope(fn):
    from flask_jwt import current_identity, _jwt

    @wraps(fn)
    def decorator(*args, **kwargs):
        ret = fn(*args, **kwargs)
        usr = get("User", "uid", current_identity['uid'])
        if 200 <= ret.status_code < 300:
            ret.properties["access_token"] = _jwt.jwt_encode_callback(
                usr).decode("utf-8")
        return ret
    return decorator


def get_scoped_info(info):
    from flask_jwt import current_identity
    behalf = current_identity.get("on_behalf_of")
    return behalf.get(info) if behalf else current_identity.get(info)


def get_request_id():
    """ Allow admins to do actions on behalf of customers. """
    return get_scoped_info("uid")


def identity(payload):
    user = get("User", "uid", payload['uid'])
    data = payload_handler(user)
    obo = {'on_behalf_of': data}
    payload.update(obo)
    return payload
