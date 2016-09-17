class GoogleException(Exception):
    def __init__(self, code: str, message: str):
        self._code = code
        self._message = message

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    def __repr__(self):
        return '%s: %s' % (self.code, self.message)

    __str__ = __repr__


class OperationException(GoogleException):
    def __init__(self, code: str, message: str):
        super(self).__init__(code, message)


class ResourceException(Exception):
    def __init__(self, code: str, message: str):
        super(self).__init__(code, message)


class ResourceNotFoundException(ResourceException):
    def __init__(self, code: str, message: str):
        super(self).__init__(code, message)


class ResourceAccessDeniedException(ResourceException):
    def __init__(self, code: str, message: str):
        super(self).__init__(code, message)
