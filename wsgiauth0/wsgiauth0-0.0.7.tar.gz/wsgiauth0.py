"""WSGI Auth0 middleware that check for HS256 and RS256 JWT.

Encoded JWT are expected in `Authorizaion` http header, ex::

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.....

"""
from collections import namedtuple
import logging

from jose import jwt, jws
from jose.exceptions import JWTError
from jose.utils import base64url_decode
import yaml

log = logging.getLogger(__name__)

Client = namedtuple('Client', 'label id audience secret')
Secret = namedtuple('Secret', 'type value')


def factory(application, config=None, **kwargs):
    monkeypatch_jws_get_keys()
    config = config.copy() if config else {}
    config.update(kwargs)
    app = auth0_middleware(application, config)
    return app


class Error(Exception):

    def __init__(self, code, description):
        super(Exception, self).__init__(code, description)

    def __repr__(self):
        return '<%s code="%s">' % (self.__class__, self.args[0])

    def to_dict(self):
        return {'code': self.args[0], 'description': self.args[1]}


def auth0_middleware(application, config):
    log.info('Setup auth0_middleware')
    log.debug('application=%s config=%s', application, config)

    clients = get_auth0_clients_config(config)

    def app(environ, start_response):
        authorization = environ.get('HTTP_AUTHORIZATION')
        jwt_environ = validate_jwt_claims(clients, authorization)
        environ.update(jwt_environ)
        return application(environ, start_response)

    return app


def validate_jwt_claims(clients, authorization):
    claims = None
    jwt_environ = {}
    if not authorization:
        jwt_environ['JWT_CLAIMS'] = None
        jwt_environ['JWT_AUTH0_CLIENT'] = None
        jwt_environ['JWT_ERROR'] = {
            'code': 'no_authorization',
            'description': 'No authorization in headers.',
        }
    else:
        client = None
        try:
            token = extract_token(authorization)
            client = extract_client(clients, token)
            claims = jwt.decode(
                token,
                client.secret.value,
                audience=client.audience,
            )

        except Error as jwt_error:
            log.debug('Jwt validation error="%r"', jwt_error)
            jwt_environ['JWT_CLAIMS'] = None
            jwt_environ['JWT_ERROR'] = jwt_error.to_dict()
        else:
            jwt_environ['JWT_CLAIMS'] = claims
            jwt_environ['JWT_ERROR'] = None

        if client is not None:
            jwt_environ['JWT_AUTH0_CLIENT'] = client._asdict()
        else:
            jwt_environ['JWT_AUTH0_CLIENT'] = None

        if claims is not None and 'sub' in claims:
            jwt_environ['REMOTE_USER'] = claims['sub']

    log.debug(
        'JWT_ERROR=%s JWT_CLAIMS=%s JWT_AUTH0_CLIENT=%s',
        jwt_environ['JWT_ERROR'],
        jwt_environ['JWT_CLAIMS'],
        jwt_environ['JWT_AUTH0_CLIENT'],
    )
    return jwt_environ


def get_auth0_clients_config(config):
    client_settings = client_settings_from_yaml(config)

    clients = {}

    for label, client_dict in client_settings:
        try:
            secret_type = client_dict['secret']['type']
            secret_value = client_dict['secret']['value']
            client_id = client_dict['id']
            audience = client_dict['audience']
        except (TypeError, KeyError):
            raise Error(
                'missing_config_key',
                'Client config missing key client_dict.',
            )

        if secret_type == 'base64_url_encoded':
            secret_value = base64url_decode(secret_value)

        client = Client(
            label=label,
            id=client_id,
            secret=Secret(type=secret_type, value=secret_value),
            audience=audience,
        )

        clients[client.id] = client

    return clients


def client_settings_from_yaml(config):
    try:
        yaml_config_path = config['clients_config_file']
    except (KeyError, TypeError):
        raise Error(
            'missing_config',
            '"clients_config_file" key not found in config',
        )

    try:
        with open(yaml_config_path) as f:
            settings = yaml.load(f)
    except Exception:
        raise Error(
            'invalid_config_file',
            'Not able to read yaml data from file path="%s"'
            % yaml_config_path,
        )

    try:
        client_settings = settings.items()
    except AttributeError:
        raise Error(
            'invalid_config_format',
            'Expects a top level dict, got %s.' % type(settings),
        )
    return client_settings


def extract_token(authorization):
    parts = authorization.split()

    if len(parts) != 2:
        raise Error(
            'invalid_header',
            'Authorization header must be "Bearer token".',
        )

    if parts[0].lower() != 'bearer':
        raise Error(
            'invalid_header',
            'Authorization header must start with "Bearer".',
        )

    return parts[1]


def extract_client(clients, token):
    try:
        claims = jwt.get_unverified_claims(token)
    except JWTError:
        raise Error('invalid_token', 'Error decoding token claims.')

    try:
        audience = claims['aud']
    except KeyError:
        raise Error('invalid_claims', 'No key aud in claims.')

    if audience in clients:
        return clients[audience]

    try:
        subject = claims['sub']
    except KeyError:
        raise Error('invalid_claims', 'No key sub in claims.')

    if subject in clients:  # pragma: no cover
        return clients[subject]

    raise Error('invalid_client', 'No config found for this client.')


def monkeypatch_jws_get_keys():  # pragma: no cover
    # Monkey patch jws._get_keys to avoid failing with a base64 decoded secret
    original_get_keys = jws._get_keys

    def jws_get_keys(key):
        if isinstance(key, bytes):
            return (key, )
        return original_get_keys(key)

    jws._get_keys = jws_get_keys
