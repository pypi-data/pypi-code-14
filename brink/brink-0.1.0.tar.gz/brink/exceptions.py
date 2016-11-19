from aiohttp.web import HTTPBadRequest, HTTPUnauthorized, HTTPNotFound


class UndefinedSchema(Exception):

    pass


class ValidationError(Exception):

    def __init__(self, errors):
        self.errors = errors


class UnexpectedDbResponse(Exception):

    pass

