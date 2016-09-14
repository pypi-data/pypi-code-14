from abc import ABCMeta, abstractmethod

from messenger_sdk import events
from messenger_sdk.fb_response import FbResponse


class Middleware(metaclass=ABCMeta):
    @property
    def supported_events(self):
        return [events.MessageEvent, events.PostbackEvent]


class EventMiddleware(Middleware):
    @abstractmethod
    def process_event(self, event: events.Event):
        raise NotImplementedError()


class ResponseMiddleware(Middleware):
    @abstractmethod
    def process_response(self, event: events.Event, response: FbResponse):
        raise NotImplementedError()
