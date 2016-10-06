import dependency_injector.containers as containers
import dependency_injector.providers as providers

from messenger_sdk.config import Config
from messenger_sdk.api_client import ApiClient
from messenger_sdk.events import EventFactory
from messenger_sdk.fb_manager import FbManager
from messenger_sdk.log import Log
from messenger_sdk.handler import BaseHandler
from messenger_sdk.middlewares.sender_action import TypingOnAction


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Singleton(Config)
    api_client = providers.Factory(ApiClient)
    event_factory = providers.Singleton(EventFactory)
    log = providers.Singleton(Log, config)
    fb_manager = providers.Factory(FbManager, api_client, config)

    typing_on_action = providers.Factory(TypingOnAction, config)

    base_middlewares = [
        {'class': typing_on_action, 'priority': 90},
    ]

    base_request_handler = providers.Factory(BaseHandler,
                                             event_factory=event_factory,
                                             fb_manager=fb_manager,
                                             base_middlewares=base_middlewares)
