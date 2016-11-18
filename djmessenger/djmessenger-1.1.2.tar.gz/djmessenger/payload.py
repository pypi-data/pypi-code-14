# -*- coding: utf-8 -*-
"""
=======
Payload
=======

:class:`.Payload` object is being used in both **handlers** and **repliers**,
it starts with you, as the BOT, replies the user buttons or quick replies, each
of them may contain a payload.

:class:`.Payload` is represented in Facebook callback as a simple string,
however, in order for BOT to better handle it, we are going to treat it as a
valid json string.

A payload contains key-value pairs that are dependant to your business logic,
as a result, you will need to write your own payload if you'd like to send
buttons and replies.

:class:`.Payload` class provides a `get_instance()` classmethod that simply
take a json string and try to deserialize it back to an instance of the actual
subclass.

Here is a quick example, let's say you want to display your products when the
user sends you a simple text "products", what you need to do is

1. Define routing policy

    In your routing policy, specify :class:`djmessenger.filtering.SimpleTextRegexFilter`
    and provide regex as "^products$" as a filter for `SIMPLE_TEXT`

2. Custom Replier

    Write a custom replier which extends either :class:`djmessenger.replying.BaseButtonReplier`
    or :class:`djmessenger.replying.BaseQuickReplyReplier` and provide payload
    that contains your product info, something like

        | Make sure you call `super().__init__()`

    ::

        class MyProductPayload(Payload):
            def __init__(self, name, price):
                super().__init__()
                self.name = name
                self.price = price


    when you're replying, this payload will be serialized into a single string
    and sent along with the template.

    Please see :class:`djmessenger.replying.BaseButtonReplier` and
    :class:`djmessenger.replying.BaseQuickReplyReplier` for more details

    The main difference between buttons and quick replies are:

    1. Buttons can only have 3 at a time
    2. Quick Replies can have 10 at a time
    3. When user clicks on Buttons, it generates a :class:`djmessenger.receiving.Postback`
    4. When user clicks on quick replies, it generates a :class:`djmessenger.receiving.QuickReply`

3. Custom handler

    If you want to do something when user clicks on the buttons or quick replies
    (which you most likely would, otherwise why sent buttons, right), you need
    to implement a custom handler which extends either :class:`djmessenger.handling.BaseQuickReplyHandler`
    or :class:`djmessenger.handling.BasePostbackHandler`.

    Both of them defines a method `get_payload()` which will return you an
    instance of `MyProductPayload`, at this point you know which user (PSID)
    clicks on which button (payload) and you can do something like saving to
    database

4. Replier

    Then you can use built-in sender or custom sender again to send something
    back to the user


"""
from djmessenger.utils.serializable import Serializable
from djmessenger.utils.utils import load_class
from abc import ABC
import json
import logging


logger = logging.getLogger(__name__)


class Payload(Serializable, ABC):
    """
    Your customized Payload subclass must extend this class and MAKE SURE that
    you call **super().__init__** in your `__init__()`
    """
    PAYLOAD_CLASS_ATTRIBUTE = 'payload_class'

    def __init__(self):
        # this is to provide info when we deserialize the callback payload so
        # that we know which class to use to deserialize the json string
        self.payload_class = '%s.%s' % (self.__module__, self.__class__.__name__)

    def get_class(self):
        """

        :return: the Payload subclass
        :rtype: class
        """
        return load_class(self.payload_class)

    def is_valid(self):
        """
        Facebook restricts that payload string can not exceed 1000 chars

        :return: True if the serialized string is less than or equal to 1000;
                 False otherwise
        :rtype: bool
        """
        return len(self.serialize()) <= 1000

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return repr(self)

    @classmethod
    def get_instance(cls, json_data):
        """
        This class method takes either a string in json format or a dict that
        represents a subclass of Payload. Since all payload subclass must
        subclass Payload and each of them has payload_class defined, we can
        easily determine what is the exact payload class and load the data and
        return an instance of that subclass

        :param json_data: string or dict that represents the subclass of Payload
        :type json_data: str or dict

        :return: an instance of the subclass of Payload
        :type: subclass of Payload
        @raise ValueError: 1. json_data is empty
                           2. json_data is neither str nor dict
                           3. json_data load failed
                           4. json_data load successfully but does not load as
                              a dict
                           5. loaded json_data but it doesn't contain
                              payload_class attribute
                           6. unable to deserialize it back to the Payload
                              subclass
        @raise ImportError: load_class failed
        @raise AttributeError: load_class failed
        """
        if not json_data:
            raise ValueError('Given json_data is empty')
        if isinstance(json_data, dict):
            pass
        elif isinstance(json_data, str):
            # json_data is a str, load it
            json_data = json.loads(json_data)
            if not isinstance(json_data, dict):
                raise ValueError('Given json data [%s] does not load to a dict'
                                 % json_data)
        else:
            raise ValueError('Given json data must either be of type str or '
                             'dict, but was %s' % type(json_data))
        # now we have json_data as a dict
        # 1. check if there is PAYLOAD_CLASS_ATTRIBUTE key
        logger.debug('Ready to check what type of this bad boy is %s' %
                     json_data)
        if Payload.PAYLOAD_CLASS_ATTRIBUTE not in json_data:
            msg = 'The json data does not contain payload_class key, which ' \
                  'indicates either this string is incorrectly formatted or ' \
                  'the string is not meant to be a Payload. data = %s' \
                  % json_data
            logger.error(msg)
            raise ValueError(msg)
        # now we have PAYLOAD_CLASS_ATTRIBUTE, we can load the class
        subpayload = load_class(json_data[Payload.PAYLOAD_CLASS_ATTRIBUTE])
        if not issubclass(subpayload, Payload):
            msg = 'payload should be a subclass of Payload class, but was %s' \
                  % type(subpayload)
            logger.error(msg)
            raise ValueError(msg)
        logger.debug('Successfully identified the subclass of Payload for this'
                     ' json data is %s' % subpayload.__name__)
        # now we have the exact class, simply deserialize using it
        instance = subpayload.deserialize(json_data)
        logger.debug('Successfully deserialized payload class %s from data'
                     '%s' % (subpayload.__name__, json_data))
        return instance


class PersistentMenuOnePayload(Payload):
    pass


class PersistentMenuTwoPayload(Payload):
    pass


class PersistentMenuThreePayload(Payload):
    pass


class PersistentMenuFourPayload(Payload):
    pass


class PersistentMenuFivePayload(Payload):
    pass


class GetStartedPayload(Payload):
    pass
