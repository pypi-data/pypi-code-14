# -*- coding: utf-8 -*-
"""
In a nutshell, we have receiving module which is responsible for converting
incoming message to a Callback object; then we have handling module to handle
internal bookkeeping for Messaging object (which is inside Callback); lastly
we use sender module to send something back.

But we need a mechanism to glue them together so that the system knows which
sender(s) should be invoked when we received some kinds of Messaging
"""
import importlib
import logging

from djmessenger.utils.serializable import Serializable
from djmessenger.utils.utils import load_class
from djmessenger.settings import DJM_ROUTING_POLICY
from djmessenger.handling import UserProfileHandler


logger = logging.getLogger(__name__)


class TargetClass(Serializable):
    def __init__(self, name, args=dict()):
        self.name = name
        self.args = args

    def get_class(self):
        return load_class(self.name)

    def get_args(self):
        # args could be none if the policy file does not specify it, which is
        # valid
        return getattr(self, 'args', {})

    def __repr__(self):
        return 'class %s with args %s' % (self.name, getattr(self, 'args', {}))

    def __str__(self):
        return repr(self)


class TargetSenderClass(TargetClass):
    pass


class TargetHandlerClass(TargetClass):
    custom_obj_map = {
        'senders': [TargetSenderClass, list]
    }

    def __init__(self, name, args=list(), senders=list()):
        super().__init__(name, args)
        self.senders = senders


class Router(Serializable):
    custom_obj_map = {
        'handlers': [TargetHandlerClass, list]
    }

    def __init__(self, ttype, handlers=list()):
        from djmessenger.receiving import ReceivingType

        self.type = ReceivingType.value_of(ttype)
        self.handlers = handlers

    def get_receiving_type(self):
        from djmessenger.receiving import ReceivingType

        try:
            ret = ReceivingType.value_of(self.type)
            return ret
        except KeyError as e:
            logger.error('Given type %s is not a valid receiving type [%s]' %
                         (self.type, ReceivingType.members().keys()))
            raise e


class Policy(Serializable):
    custom_obj_map = {
        'routers': [Router, list]
    }

    def __init__(self, routers=list()):
        self.routers = routers

    def get_router(self, rtype):
        for router in self.routers:
            if router.get_receiving_type() == rtype:
                return router
        return None

    def get_handlers(self, rtype):
        """
        Given a ReceivingType, get all applicable TargetHandlerClass classes

        @param rtype:
        @return:
        @rtype: list of TargetHandlerClass
        """
        from djmessenger.receiving import ReceivingType

        ret = []
        if self.get_router(ReceivingType.DEFAULT):
            for handler in self.get_router(ReceivingType.DEFAULT).handlers:
                if issubclass(handler.get_class(), UserProfileHandler):
                    ret.insert(0, handler)
                else:
                    ret.append(handler)
        if self.get_router(rtype) is not None:
            for handler in self.get_router(rtype).handlers:
                if issubclass(handler.get_class(), UserProfileHandler):
                    ret.insert(handler, 0)
                else:
                    ret.append(handler)
        return ret

    def get_senders(self, rtype, handler_class):
        for handler in self.get_handlers(rtype):
            if handler_class == handler:
                return handler.senders


try:
    policy = Policy.deserialize(DJM_ROUTING_POLICY)
except Exception as e:
    logger.error('Failed to load policy file from setting, please double check'
                 'on your settings for DJM_ROUTING_POLICY')


if __name__ == '__main__':
    print(policy)
