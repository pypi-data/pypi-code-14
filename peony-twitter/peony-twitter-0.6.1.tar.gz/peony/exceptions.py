# -*- coding: utf-8 -*-
import time

from . import utils


def get_error(data):
    """ Get the error, this is quite a vertical code """
    if data is not None:
        if 'errors' in data:
            if data['errors']:
                return data['errors'][0]


async def throw(response, **kwargs):
    """ get the response data if possible and raise an exception """
    ctype = response.headers['CONTENT-TYPE'].lower()
    data = None

    if "json" in ctype:
        try:
            data = await response.json(loads=utils.loads)
        except:
            pass

    err = get_error(data)
    if err is not None:
        if 'code' in err:
            code = str(err['code'])
            if code in errors:
                exception = errors[code]
                raise exception(response=response, data=data, **kwargs)

    if str(response.status) in statuses:
        exception = statuses[response.status]
        raise exception(response=response, data=data, **kwargs)

    # raise PeonyException if no specific exception was found
    raise PeonyException(response=response, data=data, **kwargs)


class PeonyException(Exception):
    """ Parent class of all the exceptions of Peony """

    def __init__(self, response=None, data=None, message=None):
        """
            Add the response and data attributes

        Extract message from the error if not explicitly given
        """
        if not message:
            err = get_error(data)
            if err is not None:
                if 'message' in err:
                    message = err['message']

            message = message or str(response)

        self.response = response
        self.data = data

        super().__init__(message)


class MediaProcessingError(PeonyException):
    pass


class StreamLimit(PeonyException):
    pass


def convert_int_keys(func):
    def decorated(self, key, *args, **kwargs):
        if isinstance(key, int):  # convert int keys to str
            key = str(key)

        return func(self, key, *args, **kwargs)

    return decorated


class ErrorDict(dict):
    """ A dict to easily add exception associated to a code """

    @convert_int_keys
    def __getitem__(self, key):
        return super().__getitem__(key)

    @convert_int_keys
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def code(self, code):
        def decorator(exception):
            self[code] = exception
            return exception

        return decorator


statuses = ErrorDict()
errors = ErrorDict()


@errors.code(32)
class NotAuthenticated(PeonyException):
    pass


@errors.code(34)
class DoesNotExist(PeonyException):
    pass


@errors.code(64)
class AccountSuspended(PeonyException):
    pass


@errors.code(68)
class MigrateToNewAPI(PeonyException):
    pass


@errors.code(88)
class RateLimitExceeded(PeonyException):

    @property
    def reset(self):
        return int(self.response.headers['X-Rate-Limit-Reset'])

    @property
    def reset_in(self):
        return self.reset - time.time()


@errors.code(92)
class SSLRequired(PeonyException):
    pass


@errors.code(130)
class OverCapacity(PeonyException):
    pass


@errors.code(131)
class InternalError(PeonyException):
    pass


@errors.code(135)
class CouldNotAuthenticate(PeonyException):
    pass


@errors.code(136)
class Blocked(PeonyException):
    pass


@errors.code(161)
class FollowLimit(PeonyException):
    pass


@errors.code(179)
class ProtectedTweet(PeonyException):
    pass


@errors.code(185)
class StatusLimit(PeonyException):
    pass


@errors.code(187)
class DuplicatedStatus(PeonyException):
    pass


@errors.code(215)
class BadAuthentication(PeonyException):
    pass


@errors.code(226)
class AutomatedRequest(PeonyException):
    pass


@errors.code(231)
class VerifyLogin(PeonyException):
    pass


@errors.code(251)
class RetiredEndpoint(PeonyException):
    pass


@errors.code(261)
class ReadOnlyApplication(PeonyException):
    pass


@errors.code(271)
class CannotMuteYourself(PeonyException):
    pass


@errors.code(272)
class NotMutingUser(PeonyException):
    pass


@errors.code(354)
class DMCharacterLimit(PeonyException):
    pass


@statuses.code(304)
class NotModified(PeonyException):
    pass


@statuses.code(400)
class BadRequest(PeonyException):
    pass


@statuses.code(401)
class Unauthorized(PeonyException):
    pass


@statuses.code(403)
class Forbidden(PeonyException):
    pass


@statuses.code(404)
class NotFound(PeonyException):
    pass


@statuses.code(406)
class NotAcceptable(PeonyException):
    pass


@statuses.code(410)
class Gone(PeonyException):
    pass


@statuses.code(420)
class EnhanceYourCalm(PeonyException):
    pass


@statuses.code(422)
class UnprocessableEntity(PeonyException):
    pass


@statuses.code(429)
class TooManyRequests(PeonyException):
    pass


@statuses.code(500)
class InternalServerError(PeonyException):
    pass


@statuses.code(502)
class BadGateway(PeonyException):
    pass


@statuses.code(503)
class ServiceUnavailable(PeonyException):
    pass


@statuses.code(504)
class GatewayTimeout(PeonyException):
    pass
