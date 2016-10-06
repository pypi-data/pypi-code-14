from abc import ABCMeta, abstractmethod
from datetime import datetime
from messenger_sdk.fb_response import FbResponse


class Event(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self, event):
        self._event = event
        self._propagate = True
        self._created_at = datetime.now()
        self._intent = None
        self._storage = EventStorage()
        self._response = None

    @property
    def recipient_id(self):
        return self._event.get('sender', {}).get('id')

    @property
    def intent(self):
        return self._intent

    @intent.setter
    def intent(self, intent):
        self._intent = intent

    @property
    def created_at(self):
        return self._created_at

    @abstractmethod
    def payload(self):
        raise NotImplementedError()

    @property
    def storage(self):
        return self._storage

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: FbResponse):
        if not isinstance(response, FbResponse):
            raise TypeError(
                'Response must be instance of {expected}, {given} given.'.format(expected=FbResponse.__class__.__name__,
                                                                                 given=type(response).__name__))
        self._response = response

    @property
    def propagate(self):
        return self._propagate

    def stop_propagation(self):
        self._propagate = False

    def as_dict(self):
        return {
            'userId': self.recipient_id,
            'createdAt': self.created_at,
            'type': self.__class__.__name__,
            'intent': self.intent,
            'payload': self.payload
        }


class PostbackEvent(Event):
    def __init__(self, event):
        super().__init__(event)

    @property
    def payload(self):
        return self._event.get('postback').get('payload')


class MessageEvent(Event):
    def __init__(self, event):
        super().__init__(event)

    @property
    def payload(self):
        return self._event.get('message').get('text')

    @property
    def attachments(self):
        return self._event.get('message').get('attachments')

    @property
    def is_echo(self):
        return self._event.get('message').get('is_echo')


class QuickReplyMessageEvent(MessageEvent):
    def __init__(self, event):
        super().__init__(event)

    @property
    def payload(self):
        return self._event.get('message').get('quick_reply', {}).get('payload')

    @property
    def text(self):
        return self._event.get('message').get('text')


class DeliveryEvent(Event):
    def __init__(self, event):
        super().__init__(event)

    def payload(self):
        pass


class ReadEvent(Event):
    def __init__(self, event):
        super().__init__(event)

    def payload(self):
        pass


class EventFactory(object):
    @staticmethod
    def create_event(event):
        if event.get('message'):
            if event.get('message').get('quick_reply'):
                event_class = QuickReplyMessageEvent
            else:
                event_class = MessageEvent
        elif event.get('postback'):
            event_class = PostbackEvent
        elif event.get('delivery'):
            event_class = DeliveryEvent
        elif event.get('read'):
            event_class = ReadEvent
        else:
            raise TypeError('Unsupported event.')

        return event_class(event)


class EventStorage(object):
    def update(self, dictionary: dict):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        attrs = str([x for x in self.__dict__])
        return "<EventStorage: %s>" % attrs

    def delete(self, property: str):
        self.__delattr__(property)
