import jwt
import logging
import os
import json
from datetime import datetime, timedelta
from helpers import get_client_info_from_token, get_configuration_from_file

from ferris3 import Service
import ferris3 as f3


def verify_client(self, client):
    """Function to verify Authorization."""
    if self:
        if issubclass(self.__class__, Service):
            headers = self.request_state._HttpRequestState__headers
            if 'Authorization' in headers:
                authorization_header = headers['Authorization']
                auth_type = authorization_header.split(' ')[0]
                inbound_app_id = authorization_header.split(' ')[1]
                if auth_type == 'Bearer':
                    client_info = get_client_info_from_token(inbound_app_id)
                    if 'client_id' in client_info:
                        settings = get_configuration_from_file()
                        client_settings = settings['ClientApp']
                        client_id = client_info[client_settings['Fields']['ClientId']]
                        obj_client = client.query(client.client_id == client_id).get()
                        logging.info("Client: %s" % obj_client)
                        if obj_client:
                            options = {
                                'verify_signature': True,
                                'verify_exp': getattr(obj_client, client_settings['Fields']['VerifyExpiration'])
                            }
                            decoded_token = verify_jwt_flask(inbound_app_id, obj_client, options)
                            if decoded_token:
                                if 'Origin' in headers:
                                    if ('localhost' in headers['Origin']) or 'localhost' in headers['host']:
                                        urls_white_list = getattr(obj_client, client_settings['Fields']['UrlsWhiteList'])
                                        if urls_white_list:
                                            if headers['Origin'] in urls_white_list:
                                                return obj_client
                                            else:
                                                raise f3.ForbiddenException('Forbbiden: origin is not allowed')
                                        else:
                                            raise f3.ForbiddenException('Forbbiden: client does not have configured origin hosts')
                                    else:
                                        raise f3.ForbiddenException('Unauthorized')
                                else:
                                    raise f3.ForbiddenException('Forbbiden: unknow host')
                            else:
                                raise f3.ForbiddenException('Forbbiden: invalid Authorization')
                        else:
                            raise f3.ForbiddenException('Unauthorized')
                    else:
                        raise f3.ForbiddenException('Unauthorized: Client id not provided into jwt token')
                else:
                    f3.ForbiddenException('Authentication type is not supported')
            else:
                logging.warning('Authorization header is not found')
                raise f3.ForbiddenException('Unauthorized')
        else:
            raise Exception('Unsupported class')
    else:
        raise


def verify_jwt_flask(token, client, options):
    """Verify if token is valid."""
    try:
        settings = get_configuration_from_file()
        client_settings = settings['ClientApp']
        decoded_token = jwt.decode(token, getattr(client, client_settings['Fields']['Secret']), options=options)
        return decoded_token
    except jwt.exceptions.ExpiredSignatureError, e:
        msg = "Error: %s - %s" % (e.__class__, e.message)
        logging.warning(msg)
        raise f3.ForbiddenException(403, message=e.message)

    except jwt.InvalidTokenError, e:
        logging.warning("Error in JWT token: %s" % e)
        return False


def create_jwt():
    """Create a new token."""
    if 'SECRET_TOKEN' in os.environ and 'APP_CLIENT_ID' in os.environ:
        token = jwt.encode(
            {
                'client_id': os.environ['APP_CLIENT_ID'],
                'exp': datetime.utcnow() + timedelta(minutes=60)
            },
            os.environ['SECRET_TOKEN'],
            algorithm='HS256'
        )

        return token
    else:
        raise Exception('Missing SECRET_TOKEN or/and APP_CLIENT_ID valiables.')


def create_jwt_with(payload, secret):
    """Create a new token."""
    token = jwt.encode(
        payload,
        secret,
        algorithm='HS256'
    )

    return token


def verify_client_request(client):
    """Decorator to verify requests from web clients."""
    def func(origin):
        """Inner."""
        def inner(self, *args, **kwargs):
            """Inner."""
            obj_client = verify_client(self, client)
            setattr(self, 'client', obj_client)
            return origin(self, *args, **kwargs)
        inner.__name__ = origin.__name__
        inner.__doc__ = origin.__doc__
        inner.__dict__.update(origin.__dict__)
        return inner
    return func

