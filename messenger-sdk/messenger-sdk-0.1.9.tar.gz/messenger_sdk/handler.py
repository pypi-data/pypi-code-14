import logging

from tornado import gen

from messenger_sdk.fb_response import FbResponse
from messenger_sdk.templates import Response
from messenger_sdk.fb_manager import FbManager
from messenger_sdk.events import EventFactory
from messenger_sdk.middlewares.middleware import Middleware, EventMiddleware, ResponseMiddleware


class BaseHandler:
    _custom_middlewares = list()

    def __init__(self, event_factory: EventFactory, fb_manager: FbManager, base_middlewares: list):
        self._event_factory = event_factory
        self._fb_manager = fb_manager
        self._base_middlewares = base_middlewares

    @property
    def custom_middlewares(self):
        return self._base_middlewares

    @custom_middlewares.setter
    def custom_middlewares(self, middlewares: list):
        self._custom_middlewares = middlewares

    @gen.coroutine
    def handle_entries(self, entries):
        for event in entries:
            try:
                logging.info('Input event: %s', event)
                event = self._event_factory.create_event(event)
                response = FbResponse()
                middleware_classes = self.load_middleware_classes()
                yield self.process_middlewares(middleware_classes=middleware_classes, event=event, response=response)
            except Exception as err:
                logging.error('Unable to handle event: %s', err)
                logging.debug('<--- TYPING OFF --->')
                response = FbResponse(Response(recipient_id=event.recipient_id,
                                               sender_action=Response.SENDER_ACTION_TYPING_OFF))
                yield self._fb_manager.send(response)

    @gen.coroutine
    def process_middlewares(self, middleware_classes, event, response):
        middleware_classes_count = len(middleware_classes)
        for index, middleware_class in enumerate(middleware_classes):
            if not event.propagate:
                break
            yield self._process_middleware(event=event, response=response, middleware_class=middleware_class)
            if response.send or index == middleware_classes_count - 1:
                yield self._fb_manager.send(response=response)
                response = FbResponse()

    @staticmethod
    def check_middleware_classes_list(middleware_classes: list):
        if len(middleware_classes) == 0:
            raise ValueError('Middleware classes list cannot be empty.')

        return True

    def load_middleware_classes(self):
        middlewares = self._base_middlewares + self._custom_middlewares
        self.check_middleware_classes_list(middlewares)

        return sorted(middlewares, key=lambda k: k['priority'], reverse=True)

    def check_mw_type(self, mw_instance):
        if not isinstance(mw_instance, Middleware):
            raise TypeError('Expected {expected} class, {given} given in {self_name}.'.format(
                expected=Middleware.__class__.__name__,
                given=type(mw_instance).__name__,
                self_name=self.__class__.__name__))

        return True

    @gen.coroutine
    def _process_middleware(self, event, response, middleware_class):
        mw_instance = middleware_class.get('class')()
        self.check_mw_type(mw_instance)
        if not any(isinstance(event, supported_event) for supported_event in mw_instance.supported_events):
            return
        logging.debug('<--- Middleware: {middleware_name} --->'.format(middleware_name=mw_instance.__class__.__name__))
        if isinstance(mw_instance, EventMiddleware):
            logging.debug('Executing: {function_name}()'.format(function_name=mw_instance.process_event.__name__))
            yield mw_instance.process_event(event=event)
        if isinstance(mw_instance, ResponseMiddleware):
            logging.debug('Executing: {function_name}()'.format(function_name=mw_instance.process_response.__name__))
            yield mw_instance.process_response(event=event, response=response)
