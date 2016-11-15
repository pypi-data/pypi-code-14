class CastConvertException(Exception):
    pass


class StreamNotFoundException(CastConvertException):
    pass


class FFProbeException(CastConvertException, IOError):
    pass
