# coding: utf-8
"""
================
Filtering Module
================

Filtering module defines a :class:`.BaseFilter` as the most basic abstract class
and all its subclasses provide some specific logic to filter a given
:class:`djmessenger.receiving.Messaging` object


"""
"""
# filtering module

In `should_handle()`, you look at the `Messaging` object and determine whether
this handler should handle this `Messaging`

"""
import logging
from abc import ABC, abstractmethod

from datetime import datetime

from django.core.validators import validate_email

from djmessenger.receiving import Messaging, ReceivingType
from djmessenger.utils.serializable import Serializable


logger = logging.getLogger(__name__)


class BaseFilter(Serializable):
    """
    BaseFilter is an ABC for filters, it defines an abstract method which takes
    a Messaging object and returns a bool to indicate whether this Messaging
    should be further processed
    """
    @abstractmethod
    def should_pass(self, messaging):
        """
        Takes a :class:`djmessenger.receiving.Messaging` object and determines
        whether this object should pass this filter and continue

        :param messaging: A Messaging instance to filter against
        :type messaging: djmessenger.receiving.Messaging
        :return: True if the given messaging passed this filter and should
                 continue with the next operation; False otherwise
        :rtype: bool
        """
        return True

    def __str__(self):
        return '<%s>' % self.__class__.__name__

    def __repr__(self):
        return str(self)


class LocationFilter(BaseFilter):
    """
    Pass if messaging is a Location
    """
    def should_pass(self, messaging):
        logger.debug('Ready to determine whether %s should handle this '
                     'messaging' % self.__class__.__name__)
        ret = messaging.get_receiving_type() == ReceivingType.LOCATION
        logger.debug('We check whether the messaging callback type is '
                     'MESSAGE_RECEIVED_LOCATION. The result is %s' % ret)
        return ret


class StickerFilter(BaseFilter):
    """
    Pass if messaging is a STICKER and the id is within STICKER_IDS
    """
    STICKER_IDS = tuple()

    def should_pass(self, messaging):
        logger.debug('Ready to determine whether %s should handle this '
                     'messaging' % self.__class__.__name__)
        ret = messaging.get_receiving_type() == ReceivingType.STICKER \
            and str(messaging.get_sticker_id())[-3:] in self.__class__.STICKER_IDS
        logger.debug('We determine whether we should handle the messaging by '
                     '1. check if the callback type is MESSAGE_RECEIVED_STICKER'
                     ', 2. check if the last 3 digit of sticker id is in '
                     '%s. The result is %s' % (self.__class__.STICKER_IDS, ret))
        return ret

    def __str__(self):
        return '%s with STICKER_IDS %s' % (self.__class__.__name__,
                                           self.__class__.STICKER_IDS)


class ThumbUpFilter(StickerFilter):
    STICKER_IDS = ('810', '814', '822')


class PostbackFilter(BaseFilter):
    """
    Pass if messaging is a POSTBACK
    """
    def should_pass(self, messaging):
        return messaging.get_receiving_type() == ReceivingType.POSTBACK


class SimpleTextRegexFilter(BaseFilter):
    """
    Pass if messaging has a text that matches the regex

    An example in :class:`djmessenger.utils.default_routing_policy`

    ::

        {
            "name": "djmessenger.filtering.SimpleTextRegexFilter",
            "args": {
                "regex": "^你好$"
            }
        }

    """
    def __init__(self, regex=None):
        self.regex = regex

    def should_pass(self, messaging):
        from re import compile

        if not self.regex:
            ret = len(messaging.get_text()) > 0
            logger.debug('No regex provided for SimpleTextBaseHandler, '
                         'should_handle() evaluates as %s because text [%s] was'
                         ' provided' % (ret, messaging.get_text()))
            return ret
        rex = compile(self.regex)
        res = rex.fullmatch(messaging.get_text())
        ret = res is not None and len(messaging.get_text()) > 0
        logging.debug('Given text and regex (%s, %s), should_pass() is %s' %
                      (messaging.get_text(), self.regex, ret))
        return ret

    def __str__(self):
        return '<%s (regex = %s)>' % (self.__class__.__name__, self.regex)


class MultimediaFilter(BaseFilter):
    """
    Pass if messaging is multimedia
    """
    def should_pass(self, messaging):
        receiving_type = messaging.get_receiving_type()
        return receiving_type in (ReceivingType.IMAGE, ReceivingType.AUDIO,
                                  ReceivingType.VIDEO, ReceivingType.FILE)


class AuthenticationFilter(BaseFilter):
    def should_pass(self, messaging):
        return messaging.get_receiving_type() == ReceivingType.AUTHENTICATION


class EmailFilter(BaseFilter):
    """
    Filter that the text sent by user is a valid email address
    """
    def should_pass(self, messaging):
        if messaging.get_receiving_type() != ReceivingType.SIMPLE_TEXT:
            return False
        return validate_email(messaging.get_text())


class TimeFilter(BaseFilter):
    """
    Filter that passes if the messaging timestamp is within the predefined
    time period

    An example in policy

    ::

        {
            "name": "djmessenger.filtering.TimeFilter",
            "args": {
                "start_time": "2016-1-1T00:00:00Z-0800",
                "end_time": "2017-1-1T01:00:00Z-0800"
            }
        }

    """

    FORMAT = '%Y-%m-%dT%H:%M:%SZ%z'

    def __init__(self, start_time, end_time):
        """

        :param start_time: start time in the format of 'HH:MM:SS'
        :type start_time: str

        :param end_time: end time in the format of 'HH:MM:SS'
        :type end_time: str

        :param utc_offset: The timezone for this time period by specifying the
                           offset from UTC
        :type utc_offset: int
        """
        self.start_time = start_time
        self.end_time = end_time

    def should_pass(self, messaging):
        try:
            start_timestamp = datetime.strptime(self.start_time,
                                                self.FORMAT).timestamp() * 1000
            end_timestamp = datetime.strptime(self.end_time,
                                              self.FORMAT).timestamp() * 1000
            messaging_timestamp = messaging.timestamp
            ret = start_timestamp <= messaging_timestamp <= end_timestamp
            logger.debug('TimeFilter checking %d <= %d <= %d, result is %s'
                         % (start_timestamp, messaging_timestamp, end_timestamp,
                            ret))
            return ret
        except Exception as e:
            logger.critical('%s failed to convert either start time or end time'
                            ' because %s. The expected format is %s. Please '
                            'double check the time strings given in settings '
                            'are valid'
                            % (self.__class__.__name__, e, self.FORMAT))
            return True

    def __str__(self):
        return '<%s (start time: %s, end time = %s)>' \
               % (self.__class__.__name__, self.start_time, self.end_time)
