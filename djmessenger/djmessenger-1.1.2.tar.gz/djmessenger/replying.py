# -*- coding: utf-8 -*-
"""
===============
Replying Module
===============

Similarly, this replying module is to represent the json templates that should
be used when sending something back to the user based on Facebook reference:

https://developers.facebook.com/docs/messenger-platform/send-api-reference


"""
from abc import abstractmethod

import requests
import logging

from djmessenger.exceptions import DJMInvalidConfigException
from djmessenger.models import Reply, FBUserProfile
from djmessenger.payload import Payload
from djmessenger.settings import DJM_POST_MESSAGE_URL, DJM_DEFAULT_SENDER_TEXT, DJM_BOT_PREFIX
from djmessenger.utils.serializable import SerializableEnum, Serializable
from djmessenger.utils.utils import get_class_name
from djmessenger.facebook_locales import FacebookLocale
from djmessenger.receiving import Messaging
from djmessenger.utils.utils import LocalizedString


logger = logging.getLogger(__name__)


class ReplyingType(SerializableEnum):
    pass


ReplyingType.SIMPLE_TEXT = ReplyingType('simple_text')
ReplyingType.QUICK_REPLY = ReplyingType('quick_reply')
ReplyingType.BUTTON = ReplyingType('button')
ReplyingType.IMAGE = ReplyingType('image')
ReplyingType.AUDIO = ReplyingType('audio')
ReplyingType.VIDEO = ReplyingType('video')
ReplyingType.FILE = ReplyingType('file')
ReplyingType.SENDER_ACTION = ReplyingType('sender_action')


class NotificationType(SerializableEnum):
    pass


NotificationType.REGULAR = NotificationType('REGULAR')
NotificationType.SILEN_PUSH = NotificationType('SILEN_PUSH')
NotificationType.NO_PUSH = NotificationType('NO_PUSH')


class ReplyAction(SerializableEnum):
    pass


ReplyAction.MARK_SEEN = ReplyAction('mark_seen')
ReplyAction.TYPING_ON = ReplyAction('typing_on')
ReplyAction.TYPING_OFF = ReplyAction('typing_off')


class ButtonType(SerializableEnum):
    pass


ButtonType.WEB_URL= ButtonType('web_url')
ButtonType.POSTBACK = ButtonType('postback')


class CommonReplier(Serializable):
    """
    Base class for all repliers, 2 abstract methods need to be overridden

    :func:`.CommonReplier.get_message`
    :func:`.CommonReplier.get_reply_type`

    """
    notification_type = NotificationType.REGULAR
    sender_action = None

    @abstractmethod
    def get_message(self, messaging):
        """
        Based on the attributes the class constructor constructs, this method
        returns the message body, the returned must be a dict and valid json
        object.

        When construct the request json payload, if there is any text that
         could be i18n'ed, please make sure to use

        :func:`.CommonReplier.preprocess_outgoing_string` to make sure the
        string is using correct locale

        :return:
        :rtype: dict
        """
        pass

    def reply(self, messaging, post_message_url=DJM_POST_MESSAGE_URL,
              prefix=DJM_BOT_PREFIX):
        """
        Ask the replier to reply to the psid from the given messaging

        :param post_message_url: Facebook URL to post the message
        :type post_message_url: str

        :type messaging: djmessenger.receiving.Messaging
        """
        message = '%s%s' % (prefix, self.get_message(messaging))
        if message is None:
            return
        data = {
            "notification_type": self.__class__.notification_type.name,
            "recipient": {
                "id": messaging.get_psid()
            },
            "sender_action": getattr(self.__class__.sender_action, 'name', None),
            "message": message
        }
        logger.debug('Sending %s message to user %s: %s' %
                     (self.get_reply_type(), messaging.get_psid(), data))
        status = requests.post(post_message_url,
                               headers={"Content-Type": "application/json"},
                               json=data)
        try:
            recipient = FBUserProfile.objects.get(pk=messaging.get_psid())
            try:
                reply = Reply.objects.create(recipient=recipient, data=data,
                                             type=self.get_reply_type().name)
                reply.response = status.content
                reply.status_code = status.status_code
                if status.status_code == 200:
                    logger.debug('Successfully sent message %s' % data)
                else:
                    logger.debug('Sent message %s failed with status code %d'
                                 'and failure details %s' %
                                 (data, status.status_code, status.content))
                reply.save()
            except Exception as e:
                logger.debug('Failed to create Sending object because %s' % e)
        except FBUserProfile.DoesNotExist:
            logger.debug('Recipient PSID not found in database table djm_user,'
                         ' since PSID was not found, not able to save what are '
                         'we sending')

    @abstractmethod
    def get_reply_type(self):
        """
        Return the SendingType that this Sender sends

        :return:
        :rtype: ReplyingType
        """
        pass

    @staticmethod
    def preprocess_outgoing_string(psid, localized_text):
        """
        This method take cares of any preprocessing of the outgoing text.
        More specifically, this method converts the text into the user's locale,
        if available.

        :param psid:

        :param localized_text:
        :type localized_text: LocalizedString

        :return: localized string
        :rtype: str
        """
        try:
            user = FBUserProfile.objects.get(pk=psid)
            lang = user.locale
            locale = FacebookLocale[lang]
            text = localized_text.get_text_by_locale(locale).strip()
        except KeyError:
            # can't find locale
            text = localized_text.base_string.strip()
        except Exception as e:
            text = localized_text.base_string.strip()
        return text

    def __str__(self):
        return '<%s>' % self.__class__.__name__

    def __repr__(self):
        return str(self)


class ReplyActionReplier(CommonReplier):
    """
    Send a ReplyAction
    """
    def __init__(self, action):
        super().__init__(action)

    def get_reply_type(self):
        return ReplyingType.SENDER_ACTION

    def get_message(self, messaging):
        # no message
        return ""

    def __str__(self):
        return '<%s (reply action %s)>' % (self.__class__.__name__,
                                           self.sender_action)


class SimpleMessageReplier(CommonReplier):
    """
    Send a simple text message
    """
    custom_obj_map = {
        "localized_string": (LocalizedString, object)
    }

    def __init__(self, localized_string):
        """

        :type localized_string: LocalizedString
        """
        super().__init__()
        self.localized_string = localized_string

    def get_message(self, messaging):
        text = CommonReplier.preprocess_outgoing_string(messaging.get_psid(),
                                                        self.localized_string)
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        return {"text": text}

    def get_reply_type(self):
        return ReplyingType.SIMPLE_TEXT

    def __str__(self):
        return '<%s (localized string %s)>' % (self.__class__.__name__,
                                               self.localized_string.serialize())


class DefaultMessageReplier(SimpleMessageReplier):
    """
    Sends back simple text DJM_DEFAULT_SENDER_TEXT
    """
    def __init__(self):
        super().__init__(LocalizedString(DJM_DEFAULT_SENDER_TEXT, dict()))


class MultimediaReplier(CommonReplier):
    # TODO: should work with django static???
    """
    Send back multimedia from a url

    ReplyingType.IMAGE = ReplyingType('IMAGE')
    ReplyingType.AUDIO = ReplyingType('AUDIO')
    ReplyingType.VIDEO = ReplyingType('VIDEO')
    ReplyingType.FILE = ReplyingType('FILE')
    """
    sending_type = None

    def __init__(self, url):
        super().__init__()
        self.url = url

    def get_reply_type(self):
        return self.__class__.sending_type

    def get_message(self, messaging):
        return {"attachment": {
            "type": self.get_reply_type().name.lower(),
            "payload": {
                "url": self.url
            }
        }}

    def __str__(self):
        return '<%s (url = %s)' % (self.__class__.__name__, self.url)


class ImageReplier(MultimediaReplier):
    """
    Reply an Image from url
    """
    sending_type = ReplyingType.IMAGE


class AudioReplier(MultimediaReplier):
    """
    Reply an Audio from url
    """
    sending_type = ReplyingType.AUDIO


class VideoReplier(MultimediaReplier):
    """
    Reply a Video from url
    """
    sending_type = ReplyingType.VIDEO


class FileReplier(MultimediaReplier):
    """
    Reply a File from url
    """
    sending_type = ReplyingType.FILE


class BaseButtonReplier(SimpleMessageReplier):
    """
    Facebook restricts to have 3 buttons at a time

    To reply a list of Button, you need to

    1. Define a subclass that extends :class:`djmessenger.payload.Payload`, so
       that when user clicks on a button and another request calls back, we
       have a way to determine the origin by checking which subclass of Payload
       it has
    2. Define a subclass that extends :class:`.BaseButtonReplier`
    3. Define BUTTONS class variable like this

    ::

        class MyButtonReplier(BaseButtonReplier):
            BUTTONS = {
               'button 1': 'https://www.google.com',
               'button 2': MyButtonPayload('button payload 2')
            }

    The first button will open a new window that goes to the url; while the
    second button will trigger a postback request back which contains the
    payload

    """
    LIMIT = 3
    # a dict that must be provided by subclass maps from title of the button
    # to either a url or an instance of custom Payload
    BUTTONS = {}

    class Button(Serializable):
        def __init__(self, title, url="", payload=None):
            """
            There are 2 types of buttons: web_url and postback where web_url
            button simply open the url in a browser and postback sends a
            Postback message back to the BOT

            :param title: button title
            :type title: str

            :param url: only applicable if button_type == web_url
            :type url: str

            :param payload: only applicable if button_type == postback
            :type payload: subclass of Payload.serialize()
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

    def __init__(self, localized_string):
        """
        text if the text that appears in the main body

        :param localized_string:
        :type localized_string: LocalizedString
        """
        super().__init__(localized_string)
        self.buttons = list()
        self.template_type = "button"

    def add_button(self, title, url="", payload=None):
        if not hasattr(self, 'buttons'):
            self.buttons = []
        if len(self.buttons) == BaseButtonReplier.LIMIT:
            raise DJMInvalidConfigException('Buttons can have only 3 at a time')
        button = BaseButtonReplier.Button(title, url, payload)
        self.buttons.append(button)

    def _construct(self):
        for key, value in self.__class__.BUTTONS.items():
            if isinstance(value, Payload):
                self.add_button(key, None, value)
            else:
                self.add_button(key, value)

    def get_message(self, messaging):
        bts = []
        for bt in self.buttons:
            bts.append(bt.json())
        ret = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": CommonReplier.preprocess_outgoing_string(
                        messaging.get_psid(), self.localized_string),
                    "buttons": bts
                }
            }
        }
        return ret

    def get_reply_type(self):
        return ReplyingType.BUTTON

    @classmethod
    def deserialize(cls, json_data):
        ret = super().deserialize(json_data)
        ret._construct()
        return ret


class BaseQuickReplyReplier(SimpleMessageReplier):
    """
    Facebook restricts to have 10 quick replies at a time.

    To reply a list of Quick Replies, you need to

    1. Define a subclass that extends :class:`djmessenger.payload.Payload`,
       so that when user clicks on a QR and another request calls back, we have
       a way to determine the origin by checking which subclass of Payload it
       has
    2. Define a subclass that extends :class:`.BaseQuickReplyReplier`
    3. Define QUICK_REPLIES class variable like this

    ::

        class MyQuickReplyReplier(BaseQuickReplyReplier):
            QUICK_REPLIES = {
               'qr 1': MyQuickReplyPayload('qr payload 1'),
               'qr 2': MyQuickReplyPayload('qr payload 2'),
               'qr 3': MyQuickReplyPayload('qr payload 3'),
            }

    """
    LIMIT = 10
    # a dict to override by subclass which map from quick reply representation
    # (text that will be displayed to the user) and an instance of subclass of
    # Payload
    QUICK_REPLIES = {}

    class QuickReply(Serializable):
        def __init__(self, title="", payload=None):
            """

            :param title:
            :param payload:
            :type payload: subclass of Payload.serialize()
            """
            self.title = title
            if not issubclass(type(payload), Payload):
                raise ValueError('Payload for QuickReply must be a subclass of'
                                 '%s' % get_class_name(Payload))
            self.payload = payload.serialize()
            self.content_type = "text"

    def __init__(self, localized_string):
        """
        Quick Reply is essentially a :class:`.SimpleMessageSender` with buttons,
        when you send a quick reply, the user will first see the text just like
        what they will from a SimpleMessageSender, follow by a list of buttons
        they can click on.
        Upon clicking, it is sending another SIMPLE_TEXT back to the server
        with quick_reply component

        :param localized_string:
        :type localized_string: LocalizedString
        """
        super().__init__(localized_string)
        self.quick_replies = []

    def add_quick_reply(self, title, payload):
        """
        An entry of quick reply button is represented like this as Facebook
        defined

        ::

            {
                "content_type":"text",
                "title":"Red",
                "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
            },

        content_type must be "text", so the arguments here are title and payload
        , payload must be a subclass of Payload

        """
        if not hasattr(self, 'quick_replies'):
            self.quick_replies = []
        if len(self.quick_replies) == BaseQuickReplyReplier.LIMIT:
            raise DJMInvalidConfigException('Quick Reply can only have 10')
        qr = BaseQuickReplyReplier.QuickReply(title, payload)
        self.quick_replies.append(qr)

    def get_message(self, messaging):
        data = {
            "text": CommonReplier.preprocess_outgoing_string(
                messaging.get_psid(), self.localized_string)
        }
        qrs = []
        for qr in self.quick_replies:
            qrs.append(qr.json())
        data['quick_replies'] = qrs
        return data

    def _construct(self):
        for key, value in self.__class__.QUICK_REPLIES.items():
            self.add_quick_reply(key, value)

    def get_reply_type(self):
        return ReplyingType.QUICK_REPLY

    @classmethod
    def deserialize(cls, json_data):
        ret = super().deserialize(json_data)
        ret._construct()
        return ret
