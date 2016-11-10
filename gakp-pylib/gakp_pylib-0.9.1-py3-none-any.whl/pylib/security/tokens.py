import datetime
from datetime import datetime as datetime2

import jwt

from pylib import lib


def offset_day(days):
    """
    Calculates the date `days` from now.
    @sig offset_day :: Int -> Date
    """
    return datetime2.utcnow() + datetime.timedelta(days=days)


def offset_hour(hours):
    """
    Calculates the datetime `hours` from now
    @sig offset_hour :: Int -> Date
    """
    return datetime2.utcnow() + datetime.timedelta(hours=hours)


def stamp(ttl, days=True):
    """
    Creates stamp data for marking the start and end of
    a token with ttl as time to live of the token.`days`
    determines whether the ttl is in days or hours
    @sig stamp :: Int -> {}
    """
    exp = offset_day(ttl) if days else offset_hour(ttl)
    return dict(iat=datetime2.utcnow(), exp=exp)


def encode(data, stamp, secret, algorithm='HS256'):
    """
    Uses jwt to download the given data using the stamp as security. Refer
    to the pyjwt docs for info about the `secret` and `algorithm`.
    The `data` must be JSON serializable.
    @sig encode :: {Str: a} -> {Str: Date|Str} -> Str -> Str -> Str
    """
    return jwt.encode(lib.merge_dict(data, stamp), secret, algorithm=algorithm).decode('utf-8')


def decode(token, secret, algorithm='HS256'):
    """
    Decodes what has been encoded by the encode function.
    @sig decode :: Str -> Str -> Str -> {Str: a}
    """
    return jwt.decode(token, key=secret, algorithms=[algorithm])
