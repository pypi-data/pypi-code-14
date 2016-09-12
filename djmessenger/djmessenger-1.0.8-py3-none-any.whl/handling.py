# -*- coding: utf-8 -*-
"""
# Handling module

Handling module provides abstract class and some implementation for handling a
`receiving.Messaging` object

## BaseHandler

Defines `should_handle()` and `handle()` which need to be overridden by
subclasses

In `should_handle()`, you look at the `Messaging` object and determine whether
this handler should handle this `Messaging`

In `handle()`, you just perform operations on the data provided by `Messaging`

## Provided Handlers

### DummyHandler

`should_handle()` just passes without checking anything

`handle()` does nothing

This handler is for routing policy to route a `Messaging` directly to senders

### LocationHandler

`should_handle()` if the ReceivingType is LOCATION and we have location data

`handle()` save the GPS coordinates into database

### BasePayloadHandler (TBD)

This is an ABC that defines `get_payload()`, only `ReceivingType.POSTBACK` and
 `ReceivingType.QUICK_REPLY` would have `payload`

### BasePostbackPayloadHandler (TBD)

This is an ABC that you should subclass to handle payload from
`ReceivingType.POSTBACK`

### BaseQuickReplyPayloadHandler (TBD)

This is an ABC that you should subclass to handle payload from
`ReceivingType.QUICK_REPLY`

### SaveMessagingHandler

`should_handle()`: if DJM_SAVE_MESSAGING settings is True

`handle()`: save the `Messaging` object into database

### SimpleTextBaseHandler

`should_handle()`: if the `Messaging` contains a text; if regex was provided,
text must match the regex

`handle()`: do nothing. You should subclass this class if you want to do
anything to the received SIMPLE_TEXT

### ThumbUpHandler

`should_handle()`: if we think the `Messaging` is a sticker and it is a thumb up

`handle()`: increment the thumbup count for the psid in the database

### UserProfileHandler

`should_handle()`: pass

`handle()`: if DJM_SAVE_USER_PROFILE was True, fetch user details using graph
api and save it; otherwise only save the psid

> This handler should be always in DEFAULT section of the policy, otherwise
  you won't be able to send anything back since you won't have user's psid
"""
import json
import logging
from abc import ABC, abstractmethod

import requests

from djmessenger.models import UserLocation, FBUserProfile
from djmessenger.payload import Payload
from djmessenger.receiving import Messaging, ReceivingType
from djmessenger.utils.utils import get_class_name, load_class

logger = logging.getLogger(__name__)


class BaseHandler(ABC):
    """
    BaseHandler is an abstract base class to

    1. Determine whether the given messaging object should be handled by this
       handler
    2. Actually handle it by adding something to database, or other internal
       work

    Each received messaging object will be applied to all defined handlers,
    which means you can actually do multiple stuff for a single messaging as
    long as your should_handle returns True
    """
    def __init__(self, messaging):
        """

        @param messaging:
        @type messaging: Messaging
        """
        self.messaging = messaging

    def get_psid(self):
        return self.messaging.get_psid()

    @abstractmethod
    def should_handle(self):
        """
        Whether the given messaging is applicable for this handler

        @return: True if the messaging should be handled; False otherwise
        @rtype: bool
        """
        pass

    @abstractmethod
    def handle(self):
        """
        Actually handles the messaging

        @return:
        """
        pass

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return repr(self)


class SaveMessagingHandler(BaseHandler):
    """
    This handler saves the messaging into the database for further reference
    """
    def should_handle(self):
        return True

    def handle(self):
        logger.debug('SaveMessagingHandler is saving messaging...')
        from djmessenger.models import Messaging as ModelMessaging
        ModelMessaging.objects.create(body=self.messaging.serialize(),
                                      type=self.messaging.get_receiving_type())
        logger.debug('SaveMessagingHandler successfully saved messaging')


class UserProfileHandler(BaseHandler):
    """
    Every messaging has sender.id, based on settings.DJM_SAVE_USER_PROFILE, this
    handler save user profile into database using models.FBUserProfile.

    If DJM_SAVE_USER_PROFILE was True, we fetch user profile using graph API;
    otherwise we only save user psid to the database
    """
    def should_handle(self):
        return True

    def handle(self):
        from djmessenger.models import FBUserProfile
        from djmessenger.settings import DJM_USER_DETAILS_URL, DJM_PAGE_ACCESS_TOKEN, DJM_SAVE_USER_PROFILE

        # we already checked this id exists in should_handle
        psid = self.get_psid()
        logger.debug('UserProfileHandler is handling messaging from user %s' % psid)
        try:
            FBUserProfile.objects.get(pk=psid)
            # user already exists
            logger.debug('PSID %s already exists, no need to fetch' % psid)
        except FBUserProfile.DoesNotExist:
            logger.debug('User %s does not exist, trying to create' % psid)
            if DJM_SAVE_USER_PROFILE:
                # user does not exist
                logger.debug('Because DJM_SAVE_USER_PROFILE was True, Ready to '
                             'fetch and save user details for PSID %s' % psid)
                status = requests.get(
                    DJM_USER_DETAILS_URL % psid,
                    {'access_token': DJM_PAGE_ACCESS_TOKEN}
                )
                if status.status_code != 200:
                    logger.error('Failed to fetch user details using Facebook Graph'
                                 'API for PSID %s' % psid)
                else:
                    user_detail = status.json()
                    logger.debug('Successfully fetched user profile for psid %s'
                                 ': %s'
                                 % (psid, user_detail))
                    try:
                        fp = FBUserProfile(**user_detail)
                        fp.psid = psid
                        fp.save()
                        logger.debug('Successfully handled creating user '
                                     'profile for %s' % psid)
                    except:
                        logger.debug('Failed to create FBUserProfile from user'
                                     'details: %s' % user_detail)
            else:
                # do not fetch user profile, only save psid
                logger.debug('Because DJM_SAVE_USER_PROFILE was False, only '
                             'save user PSID')
                FBUserProfile.objects.create(psid=psid)


class LocationHandler(BaseHandler):
    """
    If the user sends a location to the BOT (by click on the map pin icon next
    to thumb up), this handler saves this coordinates to the database
    """
    def should_handle(self):
        logger.debug('Ready to determine whether %s should handle this '
                     'messaging' % self.__class__.__name__)
        ret = self.messaging.get_receiving_type() == ReceivingType.LOCATION
        logger.debug('We check whether the messaging callback type is '
                     'MESSAGE_RECEIVED_LOCATION. The result is %s' % ret)
        return ret

    def handle(self):
        message = self.messaging.message
        psid = self.get_psid()
        logger.debug(
            'LocationHandler is handling messaging from user %s' % psid)
        try:
            user = FBUserProfile.objects.get(pk=psid)
            timestamp = self.messaging.timestamp if hasattr(self.messaging,
                                                            'timestamp') else None
            for atta in self.messaging.message.attachments:
                if not atta.type == 'location':
                    continue
                location = UserLocation(user=user,
                                        latitude=atta.payload.coordinates.lat,
                                        longitude=atta.payload.coordinates.long,
                                        timestamp=timestamp,
                                        mid=self.messaging.message.mid,
                                        seq=self.messaging.message.seq,
                                        url=getattr(atta, 'url', None)
                                        )
                location.save()
            logger.debug(
                'Successfully handled message containing location sent '
                'from %s' % psid)
        except FBUserProfile.DoesNotExist:
            logger.debug('No profile for psid %s, it is probably because'
                         'UserProfileHandler was not enabled.' % psid)


class ThumbUpHandler(BaseHandler):
    """
    Handles when the user sends a thumb up
    """
    def should_handle(self):
        logger.debug('Ready to determine whether %s should handle this '
                     'messaging' % self.__class__.__name__)
        ret = self.messaging.get_receiving_type() == ReceivingType.STICKER \
            and str(self.messaging.get_sticker_id())[-3:] in ('810', '814', '822')
        logger.debug('We determine whether we should handle the messaging by '
                     '1. check if the callback type is MESSAGE_RECEIVED_STICKER'
                     ', 2. check if the last 3 digit of sticker id is either '
                     '810, 814 or 822. The result is %s' % ret)
        return ret

    def handle(self):
        psid = self.get_psid()
        logger.debug('ThumbUpHandler is handling Thumbup from %s' % psid)
        try:
            user = FBUserProfile.objects.get(pk=psid)
            user.thumbups += 1
            user.save()
        except FBUserProfile.DoesNotExist:
            logger.debug('No profile for psid %s, it is probably because'
                         'UserProfileHandler was not enabled.' % psid)


class DummyHandler(BaseHandler):
    """
    This handler does nothing, just pass
    """
    def should_handle(self):
        logger.debug('DummyHandler just passes')
        return True

    def handle(self):
        pass


# TODO: how to handle postback?
class BasePayloadHandler(BaseHandler):
    """
    Postback and QuickReply contains payload, and in order to support request
    chaining, we need to provide a default base class for Postback and
    QuickReply.

    Since the payload in Postback and QuickReply is merely a simple string
    limited to 1000 chars, we can utilize this space to send some bookkeeping
    info to achieve request chaining.

    We are going to make the payload (which is a plain text) looks like a valid
    json object so that we can deserialize it back to a dict and then we can
    figure out which handler was the sender, then do corresponding actions
    """

    @abstractmethod
    def get_payload_string_from_messaging(self):
        """

        @return: the corresponding payload string from Messaging
        @rtype: str
        """
        pass

    def get_payload(self):
        """
        Payload class must be a subclass of djmessenger.utils.payload.Payload,
        and the class defines an attribute `payload_class`, we can simply load
        the class from this fully qualified class name

        @return: an instance of the subclass of Payload
        @rtype: an instance of the subclass of Payload
        """
        payload_string = self.get_payload_string_from_messaging()
        try:
            return Payload.get_instance(payload_string)
        except Exception as e:
            logger.error('payload string %s should be a serialization of a '
                         'subclass of Payload, but failed to determine the '
                         'subclass and load it because %s' % (payload_string, e))


class BasePostbackHandler(BasePayloadHandler):

    def should_handle(self):
        return self.messaging.get_receiving_type() == ReceivingType.POSTBACK \
               and self.get_payload()

    def get_payload_string_from_messaging(self):
        """

        @return: The payload portion from Messaging
        @rtype: str
        """
        return self.messaging.get_postback_payload()

    @abstractmethod
    def handle(self):
        pass


class BaseQuickReplyHandler(BasePayloadHandler):
    def should_handle(self):
        return self.messaging.get_receiving_type() == ReceivingType.QUICK_REPLY \
               and self.get_payload()

    def get_payload_string_from_messaging(self):
        return self.messaging.get_quick_reply_payload()

    def get_text(self):
        """
        quick reply will come with text which is the quick reply title

        @return:
        """
        return self.messaging.get_text()

    @abstractmethod
    def handle(self):
        pass


class SimpleTextBaseHandler(BaseHandler):
    def __init__(self, messaging, regex=None):
        super().__init__(messaging)
        self.regex = regex

    def should_handle(self):
        from re import compile

        if not self.regex:
            ret = len(self.messaging.get_text()) > 0
            logger.debug('No regex provided for SimpleTextBaseHandler, '
                         'should_handle() evaluates as %s because text [%s] was'
                         ' provided' % (ret, self.messaging.get_text()))
            return ret
        rex = compile(self.regex)
        res = rex.fullmatch(self.get_text())
        ret = res and len(self.messaging.get_text()) > 0
        logging.debug('Given text and regex (%s, %s), should_handle() is %s' %
                      (self.get_text(), self.regex, ret))
        return ret

    def get_text(self):
        return self.messaging.get_text()

    def handle(self):
        pass


class MultimediaBaseHandler(BaseHandler):
    def should_handle(self):
        receiving_type = self.messaging.get_receiving_type()
        return receiving_type in (ReceivingType.IMAGE, ReceivingType.AUDIO,
                                  ReceivingType.VIDEO, ReceivingType.FILE)

    @abstractmethod
    def handle(self):
        pass


class AuthenticationBaseHandler(BaseHandler):
    def should_handle(self):
        return self.messaging.get_receiving_type() == ReceivingType.AUTHENTICATION

    @abstractmethod
    def handle(self):
        pass


class AccountLinkingBaseHandler(BaseHandler):
    # TODO
    def should_handle(self):
        pass

    @abstractmethod
    def handle(self):
        pass


class DeliveryBaseHandler(BaseHandler):
    # TODO
    def should_handle(self):
        pass

    @abstractmethod
    def handle(self):
        pass


class ReadBaseHandler(BaseHandler):
    # TODO
    def should_handle(self):
        pass

    @abstractmethod
    def handle(self):
        pass


class EchoBaseHandler(BaseHandler):
    # TODO
    def should_handle(self):
        pass

    @abstractmethod
    def handle(self):
        pass
