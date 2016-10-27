import datetime
import decimal
import StringIO
import urllib
import urlparse
import warnings


__all__ = ['no_password_url']

# Protocol used by festing in reality. This has to be changed
# to HTTPS at some point.
PROTO = 'http'


def _build_netloc(login, password, hostname, port):
    """Build a netloc from login, password, hostname and port. (hostname is required)

    Many librairies try to implement this, they are all doing it wrong:
        * hostname can be an IPv6. `2001:db8::1` needs to built as `[2001:db8::1]`.
        * port can be a string, `http://example.com:http/` is the same as `http://example.com:80/`

    This implementation of building the netloc, supports passing hidden password with stars.
    These passwords won't get url encoded.

    Example:
        >>> _build_netloc(None, None, 'example.com', None)
        'example.com'
        >>> _build_netloc('h@c|<3r', None, 'example.com', None)
        'h%40c%7C%3C3r@example.com'
        >>> _build_netloc('login', '******', '2001:db8::1', 8080)
        'login:******@[2001:db8::1]:8080'
        >>> _build_netloc(None, 'password', 'example.net', None)
        ':password@example.net'
    """
    if not isinstance(hostname, basestring):
        raise ValueError("hostname has to be a string, cannot be none")

    buf = StringIO.StringIO()

    if login is not None:
        buf.write(urllib.quote(login))

    if password is not None:
        buf.write(':')
        buf.write(urllib.quote(password, safe='*'))

    if buf.tell() > 0:
        buf.write('@')

    hostname = urllib.quote(hostname, safe=':')
    if ':' in hostname:
        hostname = '[{}]'.format(hostname)
    buf.write(hostname)

    if port is not None:
        buf.write(':')
        buf.write(urllib.quote(str(port)))

    return buf.getvalue()


def no_password_url(url):
    """Strip the password from the url.

    Example:

        >>> no_password_url('festung://login:password@host:8080/path')
        'festung://login:********@host:8080/path'
        >>> no_password_url('festung://login@[2001:db8::2]/path')
        'festung://login@[2001:db8::2]/path'
    """
    parsed_url = urlparse.urlsplit(url)

    password = parsed_url.password
    if password is not None:
        password = '********'  # We don't want to leak the length of the password
    netloc = _build_netloc(parsed_url.username, password, parsed_url.hostname, parsed_url.port)

    return urlparse.urlunsplit((parsed_url.scheme, netloc, parsed_url.path, parsed_url.query,
                                parsed_url.fragment))


def to_http_url(url):
    """Convert a ``festung://`` url to the ``http`` url.

    Example:
        >>> to_http_url('festung://:password@example.com:2827/vault')
        'http://example.com:2827/vault'
        >>> to_http_url('festung://:password@[2001:db8::2]:2827/path')
        'http://[2001:db8::2]:2827/path'
    """
    parsed_url = urlparse.urlsplit(url)
    netloc = _build_netloc(None, None, parsed_url.hostname, parsed_url.port)
    return urlparse.urlunsplit((PROTO, netloc, parsed_url.path, parsed_url.query,
                                parsed_url.fragment))


def cast(obj):
    """Cast most python types to valid types to be serialized in JSON and passed to SQLite"""
    if obj is None or isinstance(obj, (long, int, float, basestring)):
        if isinstance(obj, float):
            warnings.warn(
                "floats are highly inaccurate. Use them at your own risk.", RuntimeWarning)
        return obj

    if isinstance(obj, decimal.Decimal):
        return str(obj)

    if isinstance(obj, datetime.datetime):
        if obj.tzinfo is None:
            warnings.warn("non-timezone aware datetime can lead to many issues.", RuntimeWarning)
        return obj.isoformat()

    if isinstance(obj, (datetime.date, datetime.time)):
        return obj.isoformat()

    raise TypeError("Unserializeable type {}".format(type(obj)))
