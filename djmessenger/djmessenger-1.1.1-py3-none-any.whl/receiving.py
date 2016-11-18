# -*- coding: utf-8 -*-
"""
# Receiving module

This module contains all classes that represent a Facebook callback.
Basically this is just models to represent the json templates that Facebook
would sent over as described here:

`Facebook Webhook Reference <https://developers.facebook.com/docs/messenger-platform/webhook-reference>`_

"""
import time
from abc import ABC, abstractmethod
from decimal import Decimal
import logging
import json

from djmessenger.utils.serializable import Serializable, SerializableEnum
from djmessenger.payload import *


logger = logging.getLogger(__name__)


class ReceivingType(SerializableEnum):
    """
    ReceivingType defines all types that will be sent by Facebook
    """
    pass

ReceivingType.SIMPLE_TEXT = ReceivingType('SIMPLE_TEXT')
ReceivingType.QUICK_REPLY = ReceivingType('QUICK_REPLY')
ReceivingType.IMAGE = ReceivingType('IMAGE')
ReceivingType.AUDIO = ReceivingType('AUDIO')
ReceivingType.VIDEO = ReceivingType('VIDEO')
ReceivingType.FILE = ReceivingType('FILE')
ReceivingType.LOCATION = ReceivingType('LOCATION')
ReceivingType.STICKER = ReceivingType('STICKER')
ReceivingType.POSTBACK = ReceivingType('POSTBACK')
ReceivingType.AUTHENTICATION = ReceivingType('AUTHENTICATION')
ReceivingType.ACCOUNT_LINKING = ReceivingType('ACCOUNT_LINKING')
ReceivingType.DELIVERED = ReceivingType('DELIVERED')
ReceivingType.READ = ReceivingType('READ')
ReceivingType.ECHO = ReceivingType('ECHO')
# this is not a real type, this is for routing.py to indicate the settings is
# not for a specific type but for all type
ReceivingType.DEFAULT = ReceivingType('DEFAULT')
# the follows are special types to handle thread settings, all of these will
# be handled by PostbackReceivedChecker
ReceivingType.PERSISTENT_MENU_ONE = ReceivingType('PERSISTENT_MENU_ONE')
ReceivingType.PERSISTENT_MENU_TWO = ReceivingType('PERSISTENT_MENU_TWO')
ReceivingType.PERSISTENT_MENU_THREE = ReceivingType('PERSISTENT_MENU_THREE')
ReceivingType.PERSISTENT_MENU_FOUR = ReceivingType('PERSISTENT_MENU_FOUR')
ReceivingType.PERSISTENT_MENU_FIVE = ReceivingType('PERSISTENT_MENU_FIVE')
ReceivingType.GET_STARTED_BUTTON = ReceivingType('GET_STARTED_BUTTON')


class MessagingChecker(ABC):
    """
    MessagingChecker is to check a messaging that ReceivingType it should be
    """
    def __init__(self, messaging):
        """

        :param messaging:
        :type messaging: djmessenger.receiving.Messaging
        """
        self.messaging = messaging

    @abstractmethod
    def check(self):
        """

        :return: Corresponding CallbackType if it passed any check; None if
                 nothing matches
        :rtype: ReceivingType
        """
        pass


class MessageReceivedChecker(MessagingChecker):
    """
    This check handles all types in MessagedReceived and MessageEcho
    """
    def check(self):
        if not hasattr(self.messaging, 'message'):
            return None
        # first check quick reply because it also has text
        if self.messaging.message is not None \
                and hasattr(self.messaging.message, 'quick_reply') \
                and self.messaging.message.quick_reply is not None \
                and self.messaging.message.quick_reply.payload:
            return ReceivingType.QUICK_REPLY
        # check sticker
        if self.messaging.message is not None \
                and hasattr(self.messaging.message, 'sticker_id') \
                and self.messaging.message.sticker_id is not None:
            return ReceivingType.STICKER
        # then check attachments
        if self.messaging.message is not None \
                and hasattr(self.messaging.message, 'attachments') \
                and self.messaging.message.attachments:
            attachments = self.messaging.message.attachments
            if len(attachments) > 0:
                attachment = attachments[0]
                atype = attachment.type
                try:
                    obj = AttachmentType.value_of(atype)
                except KeyError:
                    raise KeyError('AttachmentType invalid %s' % atype)
                if obj == AttachmentType.IMAGE:
                    return ReceivingType.IMAGE
                elif obj == AttachmentType.AUDIO:
                    return ReceivingType.AUDIO
                elif obj == AttachmentType.VIDEO:
                    return ReceivingType.VIDEO
                elif obj == AttachmentType.FILE:
                    return ReceivingType.FILE
                elif obj == AttachmentType.LOCATION:
                    return ReceivingType.LOCATION
        # check echo
        if self.messaging.message is not None \
                and hasattr(self.messaging.message, 'is_echo') \
                and self.messaging.message.is_echo is not None \
                and self.messaging.message.is_echo:
            return ReceivingType.ECHO
        # if failed, then check whether it has text in message
        if self.messaging.message is not None \
                and hasattr(self.messaging.message, 'text') \
                and self.messaging.message.text:
            return ReceivingType.SIMPLE_TEXT


class PostbackReceivedChecker(MessagingChecker):
    def check(self):
        if not hasattr(self.messaging, 'postback'):
            return None
        if self.messaging.postback is not None \
                and self.messaging.postback.payload:
            payload_string = self.messaging.postback.payload
            logger.debug('Got postback payload string: [%s], determining more '
                         'granular types' % payload_string)
            try:
                subpayload = Payload.get_instance(payload_string)
                if isinstance(subpayload, PersistentMenuOnePayload):
                    return ReceivingType.PERSISTENT_MENU_ONE
                elif isinstance(subpayload, PersistentMenuTwoPayload):
                    return ReceivingType.PERSISTENT_MENU_TWO
                elif isinstance(subpayload, PersistentMenuThreePayload):
                    return ReceivingType.PERSISTENT_MENU_THREE
                elif isinstance(subpayload, PersistentMenuFourPayload):
                    return ReceivingType.PERSISTENT_MENU_FOUR
                elif isinstance(subpayload, PersistentMenuFivePayload):
                    return ReceivingType.PERSISTENT_MENU_FIVE
                elif isinstance(subpayload, GetStartedPayload):
                    return ReceivingType.GET_STARTED_BUTTON
                else:
                    return ReceivingType.POSTBACK
            except Exception as e:
                return ReceivingType.POSTBACK


class AuthenticationChecker(MessagingChecker):
    def check(self):
        if not hasattr(self.messaging, 'optin'):
            return None
        if self.messaging.optin is not None and self.messaging.optin.ref:
            return ReceivingType.AUTHENTICATION


class AccountLinkingChecker(MessagingChecker):
    def check(self):
        if not hasattr(self.messaging, 'account_linking'):
            return None
        if self.messaging.account_linking is not None \
                and self.messaging.account_linking.status:
            return ReceivingType.ACCOUNT_LINKING


class MessageDeliveredChecker(MessagingChecker):
    def check(self):
        if not hasattr(self.messaging, 'delivery'):
            return None
        if self.messaging.delivery is not None and self.messaging.delivery.watermark:
            return ReceivingType.DELIVERED


class MessageReadChecker(MessagingChecker):
    def check(self):
        if not hasattr(self.messaging, 'read'):
            return None
        if self.messaging.read is not None and self.messaging.read.watermark:
            return ReceivingType.READ


class Sender(Serializable):
    """
    In Receiving messages, Sender represents the Facebook user who sent this
    message to your page
    """
    def __init__(self, iid):
        """
        When representing a user, these IDs are page-scoped IDs (PSID).
        This means that the IDs of users are unique for a given page.

        :param iid: user's PSID
        :type iid: str
        """
        self.id = iid


class Recipient(Serializable):
    """
    Your page
    """
    def __init__(self, iid):
        """
        :param iid: Facebook page id
        :type iid: str
        """
        self.id = iid


class Read(Serializable):
    def __init__(self, watermark, seq):
        """

        :param watermark:  All messages that were sent before this timestamp
                           were read
        :type watermark: int

        :param seq: Sequence number
        :type seq: int
        """
        self.watermark = watermark
        self.seq = seq


class Delivery(Serializable):
    def __init__(self, watermark, seq, mids=[]):
        """

        :param watermark: All messages that were sent before this timestamp
                          were delivered
        :type watermark: int

        :param seq: Sequence number
        :type seq: int

        :param mids: Array containing message IDs of messages that were
                     delivered. Field may not be present.
        :type mids: list of str

        """
        self.watermark = watermark
        self.seq = seq
        self.mids = mids


class AccountLinking(Serializable):

    def __init__(self, status, authorization_code=""):
        """

        :param status: linked or unlinked
        :type status: str

        :param authorization_code: Value of pass-through authorization_code
                                   provided in the Linking Account flow
        :type status: str
        """
        self.status = status
        self.authorization_code = authorization_code


class Optin(Serializable):
    def __init__(self, ref):
        """

        :param ref: data-ref parameter that was defined with the entry point
        :type ref: str
        """
        self.ref = ref


class Postback(Serializable):
    def __init__(self, payload):
        """

        :param payload:  payload parameter that was defined with the button
        :type payload: str
        """
        self.payload = payload


class QuickReply(Serializable):
    def __init__(self, payload):
        """

        :param payload: Custom data provided by the app
        :type payload: str
        """
        self.payload = payload


class MultimediaAttachmentPayload(Serializable):
    def __init__(self, url):
        """

        :param url: URL of the file
        :type url: str
        """
        self.url = url


class Coordinates(Serializable):
    def __init__(self, lat, llong):
        """
        lat and llong must be convertible to Decimal

        :param lat: latitude
        :type lat: number

        :param llong: longitude
        :type llong: number
        """
        self.lat = Decimal(lat)
        self.long = Decimal(llong)


class LocationAttachmentPayload(Serializable):
    custom_obj_map = {
        'coordinates': [Coordinates, object]
    }

    def __init__(self, coordinates):
        """

        :param coordinates:
        :type coordinates: Coordinates
        """
        self.coordinates = coordinates


class AttachmentType(SerializableEnum):
    pass


AttachmentType.IMAGE = AttachmentType('image')
AttachmentType.AUDIO = AttachmentType('audio')
AttachmentType.VIDEO = AttachmentType('video')
AttachmentType.FILE = AttachmentType('file')
AttachmentType.LOCATION = AttachmentType('location')


class Attachment(Serializable):
    """
    There are 2 types of Attachment payloads, LocationAttachmentPayload and
    MultimediaAttachmentPayload, so we are not providing _obj_map but need to
    override deserialize to look at self.type and determine which type of
    payload to deserialize to
    """
    def __init__(self, ttype, payload, url):
        """

        :param ttype:
        :type ttype: str
        :param payload: either MultimediaAttachmentPayload or LocationAttachmentPayload
        :type payload: MultimediaAttachmentPayload
        :type payload: LocationAttachmentPayload
        """
        self.type = ttype
        self.payload = payload
        self.url = url

    @classmethod
    def deserialize(cls, json_data):
        # FYI: 2 attachment types, so need to check on self.type to see which
        # one to use
        if 'type' not in json_data or 'payload' not in json_data:
            raise ValueError('Deserializing Attachment must have type and '
                             'payload in the json data but was missing')
        try:
            ttype = AttachmentType.value_of(json_data['type'])
        except:
            raise ValueError('Given type is not defined: %s' % json_data['type'])
        if ttype == AttachmentType.LOCATION:
            payload_clazz = LocationAttachmentPayload
        else:
            payload_clazz = MultimediaAttachmentPayload
        url = getattr(json_data, 'url', None)
        return cls(json_data['type'],
                   payload_clazz.deserialize(json_data['payload']),
                   url
                   )


class Message(Serializable):
    """
    Each Messaging could have 1 Message object
    """
    custom_obj_map = {
        'quick_reply': [QuickReply, object],
        'attachments': [Attachment, list]
    }

    def __init__(self, text, mid, seq, sticker_id=None, quick_reply=None, attachments=[],
                 is_echo=False, app_id="", metadata=""):
        """

        :param text: text of message
        :type text: str

        :param mid: message ID
        :type mid: str

        :param seq: message sequence number
        :type seq: int

        :param quick_reply: optional custom data provided by the sending app
        :type quick_reply: QuickReply

        :param attachments: Array containing attachment data
        :type attachments: list(Attachment)

        :param is_echo: Indicates the message sent from the page itself
        :type is_echo: bool

        :param app_id: ID of the app from which the message was sent
        :type app_id: str

        :param metadata: Custom string passed to the Send API as the metadata field
        :type metadata: str

        :param sticker_id: if user sends a sticker like thumb up
        :type sticker_id: int
        """
        self.text = text
        self.mid = mid
        self.seq = seq
        self.quick_reply = quick_reply
        self.attachments = attachments
        self.is_echo = is_echo
        self.app_id = app_id
        self.metadata = metadata
        self.sticker_id = sticker_id


class Messaging(Serializable):
    """
    Each Entry contains multiple Messaging object, Messaging has different
    CallbackType, we are going to define this class so that it includes all
    possible objects and then when we got a json data, we just load them
    into the objects. After we deserialized json data into Messaging, we then
    determine what type of a Callback this is by looking at some fields and
    values using CallbackTypeChecker
    """
    custom_obj_map = {
        'sender': [Sender, object],
        'recipient': [Recipient, object],
        'message': [Message, object],
        'postback': [Postback, object],
        'optin': [Optin, object],
        'account_linking': [AccountLinking, object],
        'delivery': [Delivery, object],
        'read': [Read, object]
    }

    def __init__(self, sender, recipient, timestamp=int(time.time()),
                 message=None, postback=None, optin=None, account_linking=None,
                 delivery=None, read=None):
        """

        :param sender: Sender object
        :type sender: Sender

        :param recipient: Recipient object
        :type recipient: Recipient

        :param timestamp: epoch
        :type timestamp: int

        :param message: message block
        :type message: Messaging

        :param postback: postback block
        :type postback: Postback

        :param optin: optin block
        :type optin: Optin

        :param account_linking: account_linking block
        :type account_linking: AccountLinking

        :param delivery: delivery block
        :type delivery: Delivery

        :param read: read block
        :type read: Read
        """
        self.sender = sender
        self.recipient = recipient
        self.timestamp = timestamp
        self.message = message
        self.postback = postback
        self.optin = optin
        self.account_linking = account_linking
        self.delivery = delivery
        self.read = read
        self._receiving_type = None

    def __repr__(self):
        return 'Messaging sent from %s ReceivingType = %s' \
               % (self.get_psid(), self.get_receiving_type())

    def __str__(self):
        return repr(self)

    def get_receiving_type(self):
        """
        After loading the json data into this object, try to determine what
        type of callback this messaging is

        :return:
        :rtype: ReceivingType
        """
        if hasattr(self, '_callback_type') and self._receiving_type:
            return self._receiving_type
        # we want to first see if messaging is a MessageReceived
        res = MessageReceivedChecker(self).check()
        # loop through all subclasses of MessagingCheck and if any of it passed
        # return it
        if res:
            self._receiving_type = res
        else:
            for clazz in MessagingChecker.__subclasses__():
                res = clazz(self).check()
                if res:
                    self._receiving_type = res
        return self._receiving_type

    def get_text(self):
        """

        :return:
        :rtype: str
        """
        if hasattr(self, 'message') and hasattr(self.message, 'text') \
                and self.message.text:
            return self.message.text

    def get_url(self):
        """

        :return:
        :rtype: str
        """
        if hasattr(self, 'message') \
                and hasattr(self.message, 'attachments') \
                and len(self.message.attachments) > 0 \
                and hasattr(self.message.attachments[0], 'payload') \
                and hasattr(self.message.attachments[0].payload, 'url'):
            return self.message.attachments[0].payload.url

    def get_coordinates(self):
        """

        :return:
        :rtype: Coordinates
        """
        if hasattr(self, 'message') \
                and hasattr(self.message, 'attachments') \
                and len(self.message.attachments) > 0 \
                and hasattr(self.message.attachments[0], 'payload') \
                and hasattr(self.message.attachments[0].payload, 'coordinates'):
            return self.message.attachments[0].payload.coordinates

    def get_postback_payload(self):
        """

        :return:
        :rtype: str
        """
        if hasattr(self, 'postback') \
                and hasattr(self.postback, 'payload'):
            return self.postback.payload

    def get_quick_reply_payload(self):
        if hasattr(self, 'message') \
                and hasattr(self.message, 'quick_reply') \
                and hasattr(self.message.quick_reply, 'payload'):
            return self.message.quick_reply.payload

    def get_watermark(self):
        pass

    def get_psid(self):
        if hasattr(self, 'sender') \
                and hasattr(self.sender, 'id') \
                and self.sender.id:
            return self.sender.id

    def get_sticker_id(self):
        if hasattr(self, 'message') \
                and hasattr(self.message, 'sticker_id') \
                and self.message.sticker_id:
            return self.message.sticker_id


class Entry(Serializable):
    """
    https://developers.facebook.com/docs/messenger-platform/webhook-reference

    """
    custom_obj_map = {
        'messaging': [Messaging, list]
    }

    def __init__(self, iid, time, messaging=[]):
        """

        :param iid: page id
        :type iid: str

        :param time: time of update (epoch time in milliseconds)
        :type time: int

        :param messaging: Array of Messaging
        :type messaging: list(Messaging)
        """
        self.id = iid
        self.time = time
        # messaging is a list of Messaging object
        self.messaging = messaging


class Callback(Serializable):
    """
    https://developers.facebook.com/docs/messenger-platform/webhook-reference
    """
    custom_obj_map = {
        'entry': [Entry, list]
    }

    def __init__(self, object='page', entry=[]):
        """

        :param object: must be "page"
        :type object: str

        :param entry: list of Entry
        :type entry: list(Entry)
        """
        self.object = object
        # entry is a list of Entry objects
        self.entry = entry

    def get_sender_id(self):
        """
        Each callback must have some Messaging, we should expect that we can
        always get a sender id

        :return:
        """
        ret = None
        for entry in self.entry:
            for messaging in entry.messaging:
                if hasattr(messaging, 'sender') \
                        and hasattr(messaging.sender, 'id') \
                        and messaging.sender.id:
                    return messaging.sender.id

    @classmethod
    def get_instance(cls, request):
        """

        :param request: HTTP Request object
        :type request: django.core.handlers.wsgi.WSGIRequest
        :return: instance of Callback
        :rtype: Callback
        """
        body = request.body.decode('utf-8')
        incoming_msg = json.loads(body)
        logger.debug('Got a callback message raw: %s' % incoming_msg)
        callback = Callback.deserialize(incoming_msg)
        return callback
