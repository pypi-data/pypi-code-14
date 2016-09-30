import json


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
        super(OperationException, self).__init__(code, message)


class ResourceException(Exception):
    def __init__(self, code: str, message: str):
        super(ResourceException, self).__init__(code, message)


class ResourceNotFoundException(ResourceException):
    def __init__(self, code: str, message: str):
        super(ResourceNotFoundException, self).__init__(code, message)


class ResourceAccessDeniedException(ResourceException):
    def __init__(self, code: str, message: str):
        super(ResourceAccessDeniedException, self).__init__(code, message)


def translate_exception(e: Exception):
    if hasattr(e, "content"):
        content = json.loads(e.content.decode())
        if content['error']:
            code = content['error']['code']
            message = content['error']['message']
            if code == 404:
                raise ResourceNotFoundException(code, message) from e
            elif code == 403:
                raise ResourceAccessDeniedException(code, message) from e
            else:
                raise ResourceException(code, message) from e
    raise ResourceException('-1', "Unknown error has occurred") from e


def check_operation_status(operation_result):
    if operation_result['status'] == 'DONE':
        if 'warnings' in operation_result:
            [print('WARN -> %s: %s' % (warn['code'], warn['message'])) for warn in operation_result['warnings']]

        if 'error' in operation_result:
            error = operation_result['error']
            if 'code' in error and 'message' in error:
                raise OperationException(error['code'], error['message'])
            elif 'errors' in error:
                error = error['errors'][0]
                raise OperationException(error['code'], error['message'])
            else:
                raise OperationException('-1', 'Unknown error: ' + json.dumps(error))
        else:
            return operation_result
    else:
        return None
