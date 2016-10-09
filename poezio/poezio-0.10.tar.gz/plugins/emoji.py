from poezio.plugin import BasePlugin
import logging
log = logging.getLogger(__name__)

MAPPING = [
    ('\u2323', ':)')
]

class Plugin(BasePlugin):
    def init(self):
        self.api.add_event_handler('conversation_msg', self.handler)
        self.api.add_event_handler('private_msg', self.handler)
        self.api.add_event_handler('muc_msg', self.handler)

    def handler(self, msg, tab):
        for emoji, replacement in MAPPING:
            msg['body'] = msg['body'].replace(emoji, replacement)
