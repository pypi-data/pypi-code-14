# -*- coding: utf-8 -*-
"""
Similarly, this sending module is to represent the json templates that should
be used when sending something back to the user based on Facebook reference:

https://developers.facebook.com/docs/messenger-platform/send-api-reference

## CommonSender

`CommonSender` defines 4 attributes: `recipient`, `sender_action`,
`notification_type`, `message` because that's what [Facebook Send API](https://developers.facebook.com/docs/messenger-platform/send-api-reference) requires

And `send()` method actually sends the json string (serialized from the above
4 attributes) to Facebook endpoint using `requests` module

Each sender will definitely get its handler as its first constructor argument.
You can define your own sender to provide customized behavior and then use it
in the routing policy

## Provided Senders

### ButtonSender (TBD)

### DefaultSender

Simple sends back the text defined in `DJM_DEFAULT_SENDER_TEXT`

- args: takes no argument

### MultimediaSender

Sends back a `SendingType` with its url

    ```
    image
    audio
    video
    file
    ```

- args:
    - sending_type: image, audio, video, file
    - url: url to the resource

### QuickReplySender (TBD)

### SenderActionSender

Sends back a sender action, check [Facebook Reference](https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions)

- args:
    - action: mark_seen, typing_on, typing_off

### SimpleMessageSender

Sends back a simple text message, could be i18n'ed

- args:
    - text: message to send back to user

"""
from abc import abstractmethod

import requests
import gettext

from djmessenger.exceptions import DJMInvalidConfigException
from djmessenger.models import Sending
from djmessenger.payload import Payload
from djmessenger.receiving import Recipient
from djmessenger.settings import DJM_POST_MESSAGE_URL, DJM_DEFAULT_SENDER_TEXT, DJM_BOT_PREFIX
from djmessenger.utils.i18n import *
from djmessenger.utils.serializable import SerializableEnum, Serializable
from djmessenger.utils.utils import get_class_name
from djmessenger.handling import BaseHandler


logger = logging.getLogger(__name__)


class SendingType(SerializableEnum):
    pass


SendingType.SIMPLE_TEXT = SendingType('simple_text')
SendingType.QUICK_REPLY = SendingType('quick_reply')
SendingType.BUTTON = SendingType('button')
SendingType.IMAGE = SendingType('image')
SendingType.AUDIO = SendingType('audio')
SendingType.VIDEO = SendingType('video')
SendingType.FILE = SendingType('file')
SendingType.SENDER_ACTION = SendingType('sender_action')


class NotificationType(SerializableEnum):
    pass


NotificationType.REGULAR = NotificationType('REGULAR')
NotificationType.SILEN_PUSH = NotificationType('SILEN_PUSH')
NotificationType.NO_PUSH = NotificationType('NO_PUSH')


class SenderAction(SerializableEnum):
    pass


SenderAction.MARK_SEEN = SenderAction('mark_seen')
SenderAction.TYPING_ON = SenderAction('typing_on')
SenderAction.TYPING_OFF = SenderAction('typing_off')


class ButtonType(SerializableEnum):
    pass


ButtonType.WEB_URL= ButtonType('web_url')
ButtonType.POSTBACK = ButtonType('postback')


class CommonSender(Serializable):
    """
    Subclasses of CommonSender must remember to call super().__init__() and the
    first argument must be a handler
    """
    # excludes = ('handler',)

    def __init__(self, handler, sender_action=None,
                 notification_type=NotificationType.REGULAR.name):
        """
        Define highest level of sending template

        @param sender_action: sender action
        @type sender_action: SenderAction

        @param notification_type: mostly no need to change this, default is
                                  regular
        @type notification_type: NotificationType
        """
        assert issubclass(type(handler), BaseHandler), \
            'The first argument in CommonSender constructor must be a subclass ' \
            'of BaseHandler'
        self.recipient = Recipient(handler.get_psid())
        self.sender_action = sender_action
        self.notification_type = notification_type
        self.message = None
        self._handler = handler

    @abstractmethod
    def get_message(self):
        """
        Based on the attributes the class constructor constructs, this method
        returns the message body, the returned must be a dict and valid json
        object.

        When construct the request json payload, if there is any text that
         could be i18n'ed, please make sure to use

        `CommonSender.preprocess_outgoing_string()` to make sure the string is
        using correct locale

        @return:
        @rtype: dict
        """
        pass

    def send(self):
        self.message = self.get_message()
        data = self.json()
        logger.debug('Sending %s message to user %s: %s' %
                     (self.get_sending_type(), self.recipient.id, data))
        status = requests.post(DJM_POST_MESSAGE_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        try:
            recipient = FBUserProfile.objects.get(pk=self.recipient.id)
            try:
                sending = Sending.objects.create(recipient=recipient, data=data,
                                                 type=self.get_sending_type().name)
                sending.response = status.content
                sending.status_code = status.status_code
                if status.status_code == 200:
                    logger.debug('Successfully sent message %s' % data)
                else:
                    logger.debug('Sent message %s failed with status code %d'
                                 'and failure details %s' %
                                 (data, status.status_code, status.content))
                sending.save()
            except Exception as e:
                logger.debug('Failed to create Sending object because %s' % e)
        except FBUserProfile.DoesNotExist:
            logger.debug('Recipient PSID not found in database table djm_user,'
                         ' since PSID was not found, not able to save what are '
                         'we sending')

    @abstractmethod
    def get_sending_type(self):
        """
        Return the SendingType that this Sender sends

        @return:
        @rtype: SendingType
        """
        pass

    @classmethod
    def preprocess_outgoing_string(cls, psid, text, add_prefix=True):
        """
        This method take cares of any preprocessing of the outgoing text.
        More specifically, this method converts the text into the user's locale,
         if available.

        @param psid:
        @param text:
        @param add_prefix: whether prepend DJM_BOT_PREFIX to the start of text,
                           you might want to use it when processing button text
        @type add_prefix: bool
        @return:
        """
        install_user_locale(psid)
        try:
            if add_prefix:
                ret = _(DJM_BOT_PREFIX).encode('utf-8') + _(text).encode('utf-8')
            else:
                ret = _(text).encode('utf-8')
        except:
            # if the locale is not supported, _() will fail, so catch it and
            # fallback to English
            if add_prefix:
                ret = DJM_BOT_PREFIX.encode('utf-8') + text.encode('utf-8')
            else:
                ret = text.encode('utf-8')
        reset_locale()
        return ret

    def get_psid(self):
        return self.recipient.id


class SenderActionSender(CommonSender):
    """
    Send a Sender Action
    """
    def __init__(self, handler, action):
        super().__init__(handler, action)

    def get_sending_type(self):
        return SendingType.SENDER_ACTION

    def get_message(self):
        # no message
        return ""


class SimpleMessageSender(CommonSender):
    """
    Send a simple text message
    """
    excludes = ['text']

    def __init__(self, handler, text):
        super().__init__(handler)
        self.text = text

    def get_message(self):
        # FUTURE: we can probably move this part to CommonSender so that
        #         subclasses don't need to worry about it
        text = CommonSender.preprocess_outgoing_string(
            self.get_psid(), self.text)
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        return {"text": text}

    def get_sending_type(self):
        return SendingType.SIMPLE_TEXT


class DefaultSender(SimpleMessageSender):
    """
    Sends back simple text DJM_DEFAULT_SENDER_TEXT
    """
    def __init__(self, handler):
        super().__init__(handler, DJM_DEFAULT_SENDER_TEXT)


class MultimediaSender(CommonSender):
    # TODO: should work with django static???
    """
    Send back multimedia from a url

    SendingType.IMAGE = SendingType('IMAGE')
    SendingType.AUDIO = SendingType('AUDIO')
    SendingType.VIDEO = SendingType('VIDEO')
    SendingType.FILE = SendingType('FILE')
    """

    def __init__(self, handler, sending_type, url):
        super().__init__(handler)
        self.sending_type = sending_type
        self.url = url

    def get_sending_type(self):
        return SendingType.value_of(self.sending_type)

    def get_message(self):
        return {"attachment": {
            "type": self.get_sending_type().name.lower(),
            "payload": {
                "url": self.url
            }
        }}


class BaseButtonSender(SimpleMessageSender):
    """
    Facebook restricts to have 3 buttons at a time
    """
    LIMIT = 3

    class Button(Serializable):
        def __init__(self, title, url="", payload=None):
            """
            There are 2 types of buttons: web_url and postback where web_url
            button simply open the url in a browser and postback sends a
            Postback message back to the BOT

            @param button_type: web_url or postback
            @type button_type: ButtonType

            @param title: button title
            @type title: str

            @param url: only applicable if button_type == web_url
            @type url: str

            @param payload: only applicable if button_type == postback
            @type payload: subclass of Payload.serialize()
            """
            if not url and not payload:
                raise ValueError('url and payload can not both be empty')
            if url and payload:
                raise ValueError('url and payload are mutually-exclusive')
            self.type = ButtonType.WEB_URL if url else ButtonType.POSTBACK
            self.title = title
            if url:
                self.url = url
            if payload and not issubclass(type(payload), Payload):
                raise ValueError('Payload for Button must be a subclass of'
                                 '%s' % get_class_name(Payload))
            if payload:
                self.payload = payload.serialize()

    def __init__(self, handler, text):
        """
        text if the text that appears in the main body

        @param psid:
        @param text:
        @type text: str
        """
        super().__init__(handler, text)
        self.buttons = list()
        self.template_type = "button"

    def add_button(self, title, url="", payload=None):
        if len(self.buttons) == BaseButtonSender.LIMIT:
            raise DJMInvalidConfigException('Buttons can have only 3 at a time')
        button = BaseButtonSender.Button(
            CommonSender.preprocess_outgoing_string(self.get_psid(), title, False),
            url, payload)
        self.buttons.append(button)

    def get_message(self):
        bts = []
        for bt in self.buttons:
            bts.append(bt.json())
        ret = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": CommonSender.preprocess_outgoing_string(self.get_psid(), self.text),
                    "buttons": bts
                }
            }
        }
        return ret

    def get_sending_type(self):
        return SendingType.BUTTON


class BaseQuickReplySender(SimpleMessageSender):
    """
    Facebook restricts to have 10 quick replies at a time
    """
    LIMIT = 10

    class QuickReply(Serializable):
        def __init__(self, title="", payload=None):
            """

            @param title:
            @param payload:
            @type payload: subclass of Payload.serialize()
            """
            self.title = title
            if not issubclass(type(payload), Payload):
                raise ValueError('Payload for QuickReply must be a subclass of'
                                 '%s' % get_class_name(Payload))
            self.payload = payload.serialize()
            self.content_type = "text"

    def __init__(self, handler, text):
        """
        Quick Reply is essentially a SimpleMessageSender with buttons, then you
        send a quick reply, the user will first see the text just like what they
         will from a SimpleMessageSender, follow by a list of buttons they can
         click on. Upon clicking, it is sending another SIMPLE_TEXT back to the
         server with quick_reply component

        @param psid:
        @param text:
        """
        super().__init__(handler, text)
        self.quick_replies = []

    def add_quick_reply(self, title, payload):
        """
        An entry of quick reply button is represented like this

        ```
        {
            "content_type":"text",
            "title":"Red",
            "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
        },
        ```
        content_type must be "text", so the arguments here are title and payload
        , payload must be a subclass of Payload

        @return:
        """
        if len(self.quick_replies) == BaseQuickReplySender.LIMIT:
            raise DJMInvalidConfigException('Quick Reply can only have 10')
        qr = BaseQuickReplySender.QuickReply(title, payload)
        self.quick_replies.append(qr)

    def get_message(self):
        data = {
            "text": CommonSender.preprocess_outgoing_string(self.get_psid(),
                                                            self.text)
        }
        qrs = []
        for qr in self.quick_replies:
            qrs.append(qr.json())
        data['quick_replies'] = qrs
        return data

    def get_sending_type(self):
        return SendingType.QUICK_REPLY
