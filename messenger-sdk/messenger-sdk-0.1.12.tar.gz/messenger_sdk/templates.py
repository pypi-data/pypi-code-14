from abc import abstractmethod
from abc import ABCMeta


class Template(metaclass=ABCMeta):
    @abstractmethod
    def __dict__(self):
        raise NotImplementedError


class Response(Template):
    NOTIFICATION_TYPE_REGULAR = 'REGULAR'
    NOTIFICATION_TYPE_SILENT_PUSH = 'SILENT_PUSH'
    NOTIFICATION_TYPE_NO_PUSH = 'NO_PUSH'
    _notification_types = [NOTIFICATION_TYPE_REGULAR, NOTIFICATION_TYPE_SILENT_PUSH, NOTIFICATION_TYPE_NO_PUSH]

    SENDER_ACTION_TYPING_ON = 'typing_on'
    SENDER_ACTION_TYPING_OFF = 'typing_off'
    SENDER_ACTION_MARK_SEEN = 'mark_seen'
    _sender_actions = [SENDER_ACTION_TYPING_ON, SENDER_ACTION_TYPING_OFF, SENDER_ACTION_MARK_SEEN]

    def __init__(self, recipient_id, notification_type=None, message=None, sender_action=None):
        self._recipient_id = recipient_id
        self._message = message
        self._sender_action = sender_action
        if not notification_type and not sender_action:
            notification_type = Response.NOTIFICATION_TYPE_REGULAR
        self._notification_type = notification_type

        self.throw_if_not_valid()

    def throw_if_not_valid(self):
        if not self.message and not self.sender_action:
            raise ValueError('message or sender_action must be set.')

        if self.sender_action and self.sender_action.lower() not in self._sender_actions:
            raise ValueError(
                'Invalid sender_action. Given: {given}. Expected: {expected}.'.format(given=self.sender_action,
                                                                                      expected=self._sender_actions))
        if self.notification_type and self.notification_type.upper() not in self._notification_types:
            raise ValueError(
                'Invalid notification_type. Given: {given}. Expected: {expected}.'.format(given=self.notification_type,
                                                                                          expected=self._notification_types))
        if self.message and not isinstance(self.message, Message):
            raise TypeError(
                'Invalid message type. Expected {expected}, given {given}.'.format(expected=Message.__class__.__name__,
                                                                                   given=type(self.message).__name__))

    def __dict__(self):
        template = {
            'recipient': {
                'id': self.recipient_id
            }
        }
        if self.notification_type:
            template.update({
                'notification_type': self.notification_type.upper()
            })
        if self.message:
            template.update({
                'message': self.message.__dict__()
            })
        if self.sender_action:
            template.update({
                'sender_action': self.sender_action.lower()
            })

        return template

    @property
    def recipient_id(self):
        return self._recipient_id

    @property
    def message(self):
        return self._message

    @property
    def sender_action(self):
        return self._sender_action

    @property
    def notification_type(self):
        return self._notification_type


class TextResponse(Response):
    def __init__(self, recipient_id,
                 text,
                 notification_type=None,
                 quick_replies=None,
                 metadata=None):
        message = Message(text=text, quick_replies=quick_replies, metadata=metadata)
        super().__init__(recipient_id=recipient_id, notification_type=notification_type, message=message)


class GenericResponse(Response):
    def __init__(self, recipient_id,
                 elements: list,
                 notification_type=None,
                 quick_replies=None,
                 metadata=None):
        attachment = Attachment(type='template', payload=GenericPayload(elements=elements))
        message = Message(attachment=attachment, quick_replies=quick_replies, metadata=metadata)
        super().__init__(recipient_id=recipient_id, notification_type=notification_type, message=message)


class ButtonResponse(Response):
    def __init__(self, recipient_id,
                 text: str,
                 buttons: list,
                 notification_type=None,
                 quick_replies=None,
                 metadata=None):
        attachment = Attachment(type='template', payload=ButtonPayload(buttons=buttons, text=text))
        message = Message(attachment=attachment, quick_replies=quick_replies, metadata=metadata)
        super().__init__(recipient_id=recipient_id, notification_type=notification_type, message=message)


class FbObject(metaclass=ABCMeta):
    @abstractmethod
    def __dict__(self):
        raise NotImplementedError()

    @staticmethod
    def throw_if_greater_than_limit(value, limit: int, value_name: str):
        if value_name and not isinstance(value_name, str):
            raise TypeError('value_description must be instance of string.')
        length = len(value)
        if length > limit:
            error_message = 'Limit is {limit} - {value_name} length is {length}: {value}'.format(limit=limit,
                                                                                                 length=length,
                                                                                                 value_name=value_name,
                                                                                                 value=value[:100])
            raise ValueError(error_message)


class StructuredPayload(FbObject):
    TEMPLATE_TYPE_GENERIC = 'generic'
    TEMPLATE_TYPE_BUTTON = 'button'

    @abstractmethod
    def __dict__(self):
        raise NotImplementedError()


class Attachment(FbObject):
    TYPE_IMAGE = 'image'
    TYPE_AUDIO = 'audio'
    TYPE_VIDEO = 'video'
    TYPE_FILE = 'file'
    TYPE_TEMPLATE = 'template'
    _types = [TYPE_IMAGE, TYPE_AUDIO, TYPE_VIDEO, TYPE_FILE, TYPE_TEMPLATE]

    def __init__(self, type: str, payload: StructuredPayload):
        self._type = type
        self._payload = payload

        self.throw_if_not_valid()

    def __dict__(self):
        return {
            'type': self._type,
            'payload': self._payload.__dict__()
        }

    def throw_if_not_valid(self):
        if self._type not in self._types:
            raise ValueError(
                'Invalid type. Given: {given}. Expected: {expected}.'.format(given=self._type,
                                                                             expected=self._types))

        if not isinstance(self._payload, StructuredPayload):
            raise TypeError('Invalid payload type.')


class QuickReply(FbObject):
    CONTENT_TYPE_TEXT = 'text'
    CONTENT_TYPE_LOCATION = 'location'

    def __init__(self,
                 title=None,
                 payload=None,
                 title_limit=20,
                 payload_limit=1000,
                 content_type='text',
                 image_url=None):
        self._content_type = content_type
        self._title = title
        self._payload = payload
        self._title_limit = title_limit
        self._payload_limit = payload_limit
        self._image_url = image_url

        self.throw_if_not_valid()

    def __dict__(self):
        d = {
            'content_type': self._content_type,
            'title': self._title,
            'payload': self._payload
        }

        if self._image_url:
            d.update({'image_url': self._image_url})

        return d

    def throw_if_not_valid(self):
        if not self._content_type == QuickReply.CONTENT_TYPE_TEXT and not self._content_type == QuickReply.CONTENT_TYPE_LOCATION:
            raise ValueError('Invalid quick reply content type')

        if self._content_type == QuickReply.CONTENT_TYPE_TEXT:
            if not self._title or not self._payload:
                raise ValueError('Missing quick reply  title or payload.')
            self.throw_if_greater_than_limit(value=self._payload, limit=self._payload_limit, value_name='payload')


class Message(FbObject):
    def __init__(self, text=None, attachment=None, quick_replies=None, metadata=None,
                 text_limit=320, quick_replies_limit=10, metadata_limit=1000):
        self._text = text
        self._attachment = attachment
        self._quick_replies = quick_replies
        self._metadata = metadata
        self._text_limit = text_limit
        self._quick_replies_limit = quick_replies_limit
        self._metadata_limit = metadata_limit

        self.throw_if_not_valid()

    def __dict__(self):
        template = dict()
        if self._text:
            template.update({'text': self._text})
        if self._attachment:
            template.update({'attachment': self._attachment.__dict__()})
        if self._quick_replies:
            template.update({'quick_replies': [quick_reply.__dict__() for quick_reply in self._quick_replies]})
        if self._metadata:
            template.update({'metadata': self._metadata})

        return template

    def throw_if_not_valid(self):
        if self._attachment and self._text:
            raise ValueError('text and attachment are mutually exclusive.')

        if self._attachment:
            if not isinstance(self._attachment, Attachment):
                raise TypeError('Invali attachment type.')

        if self._quick_replies:
            if not all(isinstance(quick_reply, QuickReply) for quick_reply in self._quick_replies):
                raise TypeError('Invalid quick reply type.')
            self.throw_if_greater_than_limit(value=self._quick_replies,
                                             limit=self._quick_replies_limit,
                                             value_name='quick_replies')

        if self._metadata:
            self.throw_if_greater_than_limit(value=self._metadata, limit=self._metadata_limit, value_name='metadata')


class Button(FbObject):
    TYPE_WEB_URL = 'web_url'
    TYPE_POSTBACK = 'postback'
    TYPE_SHARE = 'element_share'
    _types = [TYPE_WEB_URL, TYPE_POSTBACK, TYPE_SHARE]

    def __init__(self, type: str, title=None, url=None, payload=None, title_limit=20, payload_limit=1000):
        self._type = type
        self._title = title
        self._url = url
        self._payload = payload
        self._title_limit = title_limit
        self._payload_limit = payload_limit

        self.throw_if_not_valid()

    def __dict__(self):
        template = {
            'type': self._type,
        }
        if self._title:
            template.update({'title': self._title})
        if self._url:
            template.update({'url': self._url})
        if self._payload:
            template.update({'payload': self._payload})

        return template

    def throw_if_not_valid(self):
        if self._type.lower() not in self._types:
            raise ValueError('Invalid type. Given: {given}. Expected: {expected}.'.format(given=self._type,
                                                                                          expected=self._types))

        if self._type.lower() != self.TYPE_SHARE and self._title is None:
            raise ValueError('Missing button title')

        if self._type.lower() == self.TYPE_SHARE:
            if self._payload:
                raise ValueError('If type is element_share, payload must be None.')
            if self._title:
                raise ValueError('If type is element_share, title must be None.')
            if self._url:
                raise ValueError('If type is element_share, url must be None.')

        if self._type.lower() == self.TYPE_WEB_URL:
            if self._payload:
                raise ValueError('If type is web_url, payload must be None.')
            if not self._url:
                raise ValueError('Url is required.')

        if self._type.lower() == self.TYPE_POSTBACK:
            if self._url:
                raise ValueError('If type is postback, web_url must be None.')
            if not self._payload:
                raise ValueError('Postback is required.')
            self.throw_if_greater_than_limit(value=self._payload, limit=self._payload_limit, value_name='payload')


class Element(FbObject):
    def __init__(self, title: str, item_url=None, image_url=None, subtitle=None, buttons=None, title_limit=80,
                 subtitle_limit=80, buttons_limit=3):
        self._title = title
        self._item_url = item_url
        self._image_url = image_url
        self._subtitle = subtitle
        self._buttons = buttons
        self._title_limit = title_limit
        self._subtitle_limit = subtitle_limit
        self._buttons_limit = buttons_limit

        self.throw_if_not_valid()

    def __dict__(self):
        template = {
            'title': self._title,
        }
        if self._item_url:
            template.update({'item_url': self._item_url})
        if self._image_url:
            template.update({'image_url': self._image_url})
        if self._subtitle:
            template.update({'subtitle': self._subtitle})
        if self._buttons:
            template.update({'buttons': [button.__dict__() for button in self._buttons]})

        return template

    def throw_if_not_valid(self):
        if self._buttons:
            self.throw_if_greater_than_limit(value=self._buttons, limit=self._buttons_limit, value_name='buttons')

        if self._buttons and not all(isinstance(button, Button) for button in self._buttons):
            raise TypeError('Invalid button type.')


class GenericPayload(StructuredPayload):
    def __init__(self, elements: list, elements_limit=10):
        self._template_type = self.TEMPLATE_TYPE_GENERIC
        self._elements = elements
        self._elements_limit = elements_limit

        self.throw_if_not_valid()

    def __dict__(self):
        template = {
            'template_type': self._template_type,
        }
        if self._elements:
            template.update({'elements': [element.__dict__() for element in self._elements]})

        return template

    def throw_if_not_valid(self):
        self.throw_if_greater_than_limit(value=self._elements, limit=self._elements_limit, value_name='elements')

        if not all(isinstance(element, Element) for element in self._elements):
            raise TypeError('Invalid element type.')


class ButtonPayload(StructuredPayload):
    def __init__(self, text: str, buttons: list, text_limit=320, buttons_limit=3):
        self._template_type = self.TEMPLATE_TYPE_BUTTON
        self._text = text
        self._buttons = buttons
        self._text_limit = text_limit
        self._buttons_limit = buttons_limit

        self.throw_if_not_valid()

    def __dict__(self):
        return {
            'text': self._text,
            'template_type': self._template_type,
            'buttons': [button.__dict__() for button in self._buttons]
        }

    def throw_if_not_valid(self):
        self.throw_if_greater_than_limit(value=self._buttons, limit=self._buttons_limit, value_name='buttons')

        if not all(isinstance(button, Button) for button in self._buttons):
            raise TypeError('Invalid button type.')


class ThreadSettings(FbObject, Template):
    SETTING_TYPE_GREETING = 'greeting'
    SETTING_TYPE_CALL_TO_ACTIONS = 'call_to_actions'
    VALID_SETTING_TYPES = [SETTING_TYPE_GREETING, SETTING_TYPE_CALL_TO_ACTIONS]

    def __init__(self, setting_type):
        self._setting_type = setting_type
        self.throw_if_not_valid()

    def __dict__(self):
        return {
            'setting_type': self._setting_type
        }

    def throw_if_not_valid(self):
        if self._setting_type not in self.VALID_SETTING_TYPES:
            raise ValueError(
                'Invalid setting_type. Given: {given}. Expected: {expected}.'.format(given=self._setting_type,
                                                                                     expected=self.VALID_SETTING_TYPES))


class GreetingText(ThreadSettings):
    def __init__(self, text: str, text_limit=160):
        self._text = text
        self._text_limit = text_limit
        super().__init__(setting_type=ThreadSettings.SETTING_TYPE_GREETING)

    def __dict__(self):
        template = {
            'greeting': {
                'text': self._text
            }
        }
        template.update(super().__dict__())

        return template

    def throw_if_not_valid(self):
        super().throw_if_not_valid()
        self.throw_if_greater_than_limit(value=self._text, limit=self._text_limit, value_name='text')


class ButtonThreadSettings(ThreadSettings):
    NEW_THREAD = 'new_thread'
    EXISTING_THREAD = 'existing_thread'
    VALID_THREAD_STATES = [NEW_THREAD, EXISTING_THREAD]

    def __init__(self, setting_type: str, thread_state: str, call_to_actions: list, call_to_actions_limit: int):
        self._thread_state = thread_state
        self._call_to_actions = call_to_actions
        self._call_to_actions_limit = call_to_actions_limit
        super().__init__(setting_type=setting_type)

    def __dict__(self):
        template = {
            'thread_state': self._thread_state,
            'call_to_actions': self.call_to_actions_template()
        }
        template.update(super().__dict__())

        return template

    @abstractmethod
    def call_to_actions_template(self):
        raise NotImplementedError()

    def throw_if_not_valid(self):
        super().throw_if_not_valid()
        if self._thread_state not in self.VALID_THREAD_STATES:
            raise ValueError(
                'Invalid setting_type. Given: {given}. Expected: {expected}.'.format(given=self._thread_state,
                                                                                     expected=self.VALID_THREAD_STATES))
        self.throw_if_greater_than_limit(value=self._call_to_actions,
                                         limit=self._call_to_actions_limit,
                                         value_name='call_to_actions')


class GetStartedButton(ButtonThreadSettings):
    def __init__(self, call_to_action_payload: str, call_to_actions_limit=1, call_to_action_payload_limit=1000):
        self._call_to_action_payload = call_to_action_payload
        self._call_to_action_payload_limit = call_to_action_payload_limit
        super().__init__(setting_type=ThreadSettings.SETTING_TYPE_CALL_TO_ACTIONS,
                         thread_state=self.NEW_THREAD,
                         call_to_actions=self.call_to_actions,
                         call_to_actions_limit=call_to_actions_limit)

    def call_to_actions_template(self):
        return [{
            'payload': self._call_to_action_payload
        }]

    @property
    def call_to_actions(self):
        call_to_actions = list()
        call_to_actions.append(self._call_to_action_payload)
        return call_to_actions

    def throw_if_not_valid(self):
        super().throw_if_not_valid()
        self.throw_if_greater_than_limit(value=self._call_to_action_payload,
                                         limit=self._call_to_action_payload_limit,
                                         value_name='payload length limit')


class MenuItem(Button):
    def __init__(self, type: str, title, url=None, payload=None):
        super().__init__(type=type, title=title, url=url, payload=payload, title_limit=30)


class PersistentMenu(ButtonThreadSettings):
    def __init__(self, call_to_actions: list, call_to_actions_limit=5):
        self._call_to_actions = call_to_actions
        self._call_to_actions_limit = call_to_actions_limit
        super().__init__(setting_type=ThreadSettings.SETTING_TYPE_CALL_TO_ACTIONS,
                         thread_state=self.EXISTING_THREAD,
                         call_to_actions=call_to_actions,
                         call_to_actions_limit=call_to_actions_limit)

    def call_to_actions_template(self):
        return [call_to_action.__dict__() for call_to_action in self._call_to_actions]

    def throw_if_not_valid(self):
        super().throw_if_not_valid()
        if not all(isinstance(call_to_action, MenuItem) for call_to_action in self._call_to_actions):
            raise TypeError('Invalid menu_item type.')
