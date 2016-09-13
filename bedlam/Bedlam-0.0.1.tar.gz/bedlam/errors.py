class BedlamError(Exception):

    status = 500

    @classmethod
    def handle(cls, start_response):
        headers = [('content-length', '0')]
        start_response(str(cls.status), headers)
        return iter([''])


class NotFound(BedlamError):

    status = '404'


class RequestError(BedlamError):

    status = '400'


class PayloadError(RequestError):

    status = '400'
