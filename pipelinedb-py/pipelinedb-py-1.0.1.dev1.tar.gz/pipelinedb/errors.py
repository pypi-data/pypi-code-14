"Core exceptions raised by the phoenix client"


class PipelineDBError(Exception):
    pass

class PipelineDBUnfoundError(PipelineDBError):
    pass


class ConnectionError(PipelineDBError):
    pass


class TimeoutError(PipelineDBError):
    pass

class NotImplementedError(PipelineDBError):
    pass


class PipelineDBCommandExecuteError(PipelineDBError):
    pass


class BusyLoadingError(ConnectionError):
    pass


class InvalidResponse(PipelineDBError):
    pass


class ResponseError(PipelineDBError):
    pass


class DataError(PipelineDBError):
    pass

