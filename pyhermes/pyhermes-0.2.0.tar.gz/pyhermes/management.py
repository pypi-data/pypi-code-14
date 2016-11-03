from pyhermes.auth import HermesAuthorization
from pyhermes.settings import HERMES_SETTINGS


class HermesManager(object):
    def __init__(self, auth):
        assert isinstance(auth, HermesAuthorization)
        self.auth_headers = auth.get_auth_headers()

    def create_or_update_topic(self, topic_info):
        raise NotImplementedError()

    def subscribe(self, topic, subscriber_info):
        raise NotImplementedError()

    def unsubscribe(self, topic, subscriber_info):
        raise NotImplementedError()
