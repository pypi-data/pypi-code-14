# -*- coding: utf-8 -*-
"""
=================
Handling Module
=================

Handling module provides abstract class and some implementation for handling a
:class:`djmessenger.receiving.Messaging` object. Handling means to do internal
operations against the ``Messaging`` object, eg. save something into database,
and etc

BaseHandler
===========

Defines `handle(messaging)` which need to be overridden by subclasses

In `handle()`, you just perform operations on the data provided by ``messaging``

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

    Actually handle it by adding something to database, or other internal
    work
    """

    @abstractmethod
    def handle(self, messaging):
        """
        Actually handles the messaging

        :param messaging: A Messaging object to handle
        :type messaging: djmessenger.receiving.Messaging
        :return: nothing
        """
        pass

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __str__(self):
        return repr(self)


class SaveMessagingHandler(BaseHandler):
    """
    This handler saves the messaging into the database for further reference
    """
    def handle(self, messaging):
        logger.debug('SaveMessagingHandler is saving messaging...')
        from djmessenger.models import Messaging as ModelMessaging
        ModelMessaging.objects.create(body=messaging.serialize(),
                                      type=messaging.get_receiving_type())
        logger.debug('SaveMessagingHandler successfully saved messaging')


class UserProfileHandler(BaseHandler):
    """
    Every messaging has sender.id, based on settings.DJM_SAVE_USER_PROFILE, this
    handler save user profile into database using models.FBUserProfile.

    If DJM_SAVE_USER_PROFILE was True, we fetch user profile using graph API;
    otherwise we only save user psid to the database
    """
    def handle(self, messaging):
        from djmessenger.models import FBUserProfile
        from djmessenger.settings import DJM_USER_DETAILS_URL, DJM_PAGE_ACCESS_TOKEN, DJM_SAVE_USER_PROFILE

        # we already checked this id exists in should_handle
        psid = messaging.get_psid()
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
    def handle(self, messaging):
        psid = messaging.get_psid()
        logger.debug(
            'LocationHandler is handling messaging from user %s' % psid)
        try:
            user = FBUserProfile.objects.get(pk=psid)
            timestamp = messaging.timestamp if hasattr(self.messaging,
                                                       'timestamp') else None
            for atta in messaging.message.attachments:
                if not atta.type == 'location':
                    continue
                location = UserLocation(user=user,
                                        latitude=atta.payload.coordinates.lat,
                                        longitude=atta.payload.coordinates.long,
                                        timestamp=timestamp,
                                        mid=messaging.message.mid,
                                        seq=messaging.message.seq,
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
    def handle(self, messaging):
        psid = messaging.get_psid()
        logger.debug('ThumbUpHandler is handling Thumbup from %s' % psid)
        try:
            user = FBUserProfile.objects.get(pk=psid)
            user.thumbups += 1
            user.save()
        except FBUserProfile.DoesNotExist:
            logger.debug('No profile for psid %s, it is probably because'
                         'UserProfileHandler was not enabled.' % psid)


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
    def get_payload_string_from_messaging(self, messaging):
        """Returns payload contained in :class:`djmessenger.receiving.Messaging`

        :type messaging: djmessenger.receiving.Messaging

        :return: the corresponding payload string from Messaging
        :rtype: str
        """
        pass

    def get_payload(self, messaging):
        """
        Payload class must be a subclass of djmessenger.utils.payload.Payload,
        and the class defines an attribute `payload_class`, we can simply load
        the class from this fully qualified class name

        :type messaging: djmessenger.receiving.Messaging

        :return: an instance of the subclass of Payload
        :rtype: an instance of the subclass of Payload
        """
        payload_string = self.get_payload_string_from_messaging(messaging)
        try:
            return Payload.get_instance(payload_string)
        except Exception as e:
            logger.error('payload string %s should be a serialization of a '
                         'subclass of Payload, but failed to determine the '
                         'subclass and load it because %s' % (payload_string, e))


class BasePostbackHandler(BasePayloadHandler):
    """
    A base class to be extended by subclass to handle custom Postback Payload
    """

    def get_payload_string_from_messaging(self, messaging):
        """

        :return: The payload portion from Messaging
        :rtype: str
        """
        return messaging.get_postback_payload()

    @abstractmethod
    def handle(self, messaging):
        pass


class BaseQuickReplyHandler(BasePayloadHandler):
    """
    A base class to be extended by subclasses to handle custom QuickReply
    payload
    """

    def get_payload_string_from_messaging(self, messaging):
        return messaging.get_quick_reply_payload()

    def get_text(self, messaging):
        """
        quick reply will come with text which is the quick reply title

        :return:
        """
        return messaging.get_text()

    @abstractmethod
    def handle(self, messaging):
        pass
