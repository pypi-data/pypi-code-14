# used when a request or the client is unauthorized
class AuthenticationError(Exception):
    pass


# used on 404 requests
class NotFoundError(Exception):
    pass
