from tornado import gen
from messenger_sdk.events import Event
from messenger_sdk.fb_response import FbResponse
from messenger_sdk.config import Config
from messenger_sdk.templates import Response

from messenger_sdk.middlewares.middleware import ResponseMiddleware


class TypingOnAction(ResponseMiddleware):
    def __init__(self, config: Config):
        self._config = config

    @gen.coroutine
    def process_response(self, event: Event, response: FbResponse):
        if self._config.get_bool_parameter('facebook', 'SENDER_ACTION'):
            template = Response(recipient_id=event.recipient_id, sender_action='typing_on')
            response.add_template(template)
            response.send = True
