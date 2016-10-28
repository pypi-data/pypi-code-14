import upfluence.log
import opbeat_wrapper


class Client(opbeat_wrapper.Client):
    def __init__(self):
        self.base_service = None

    def capture_exception(self, *args, **kwargs):
        upfluence.log.logger.error('exception:', exc_info=True)
        upfluence.log.logger.error(
            dict(self._build_base_extra(), **kwargs.get('extra', {})))
