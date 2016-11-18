# -*- coding: utf-8 -*-
"""
In a nutshell, the overall flow works like this

1. receiving module converts incoming request body to a Callback instance
2. Each Callback instance contains multiple Entry and each Entry contains
   multiple Messaging
3. For each Messaging, we are going to apply this routing policy

Each routing policy contains

1. A list of Rule
2. A rule contains a list of filters, a list of handlers and a list of repliers

    2.1 filters are responsible for determining whether the given Messaging
        is applicable for further handling, a Messaging object must pass all
        listed filters in order to reach handlers
    2.2 handlers perform internal operations against the Messaging, such like
        saving something into database and etc
    2.3 repliers reply something back to the user

See :mod:`djmessenger.utils.default_routing_policy` for sample routing policy
and more details

"""
import importlib
import logging

from djmessenger.utils.serializable import Serializable
from djmessenger.utils.utils import load_class
from djmessenger.handling import UserProfileHandler, BaseHandler
from djmessenger.filtering import BaseFilter
from djmessenger.replying import CommonReplier
from djmessenger.receiving import Messaging, ReceivingType
from djmessenger.settings import DJM_POST_MESSAGE_URL, DJM_BOT_PREFIX


logger = logging.getLogger(__name__)


class TargetClass(Serializable):
    """
    This class is a wrapper for filter, handler and replier which were defined
    in the policy file. When we are reading the policy file, we will first
    deserialize each dict using this class and this class is responsible for
    determining the exact target class and return an instance of it
    """
    BASE_CLASS = None

    def __init__(self, name, args=dict()):
        """

        :param name: This is defined in the policy file and indicates the fully
                     qualified class name so that we know how to load it
        :type name: str

        :param args: A dict that contains serialized json string for arguments
                     for the target class, if any
        :type args: dict
        """
        self.name = name
        self.args = args

    def get_class(self):
        """Loads and return the exact class from ``self.name``

        :return: A class
        :rtype: class
        """
        try:
            return load_class(self.name)
        except ImportError as e:
            logger.error('Failed to load class %s because %s' % (self.name, e))
            raise e

    def get_args(self):
        # args could be none if the policy file does not specify it, which is
        # valid
        return getattr(self, 'args', {})

    def __repr__(self):
        return '%s that wraps a %s with args %s' % (self.__class__,
                                                    self.name,
                                                    self.args)

    def __str__(self):
        return repr(self)

    def get_instance(self):
        """Return an instance of the target class, which will be an instance of
        subclass of either :class:`djmessenger.filtering.BaseFilter`,
        :class:`djmessenger.handling.BaseHandler` or :class:`djmessenger.replying.CommonReplier`

        :rtype: object
        """
        class_ = self.get_class()
        if not issubclass(class_, self.__class__.BASE_CLASS):
            logger.error('%s should get a class which is a subclass of %s, '
                         'but was %s' % (self.__class__.__name__,
                                         self.__class__.BASE_CLASS.__name__,
                                         class_.__name__))
        if self.get_args():
            return class_.deserialize(self.get_args())
        else:
            return class_()


class TargetFilterClass(TargetClass):
    BASE_CLASS = BaseFilter


class TargetReplierClass(TargetClass):
    BASE_CLASS = CommonReplier


class TargetHandlerClass(TargetClass):
    BASE_CLASS = BaseHandler


class Rule(Serializable):
    """
    A ``Rule`` is a class that will be applied to a ``Messaging`` instance.
    Each ``Rule`` contains a list of filters, a list of handlers and a list of
    repliers.

    Filters take a ``Messaging`` and determine whether this ``Messaging`` should
    proceed further, if any of the Filters returns False, this ``Rule`` will be
    skipped.

    See :mod:`djmessenger.utils.default_routing_policy` for sample routing policy
    and more details
    """
    custom_obj_map = {
        'filters': [TargetFilterClass, list],
        'handlers': [TargetHandlerClass, list],
        'repliers': [TargetReplierClass, list]
    }

    def __init__(self, ttype, name='', filters=list(), handlers=list(), repliers=list()):
        from djmessenger.receiving import ReceivingType

        self.type = ReceivingType.value_of(ttype)
        self.filters = filters
        self.handlers = handlers
        self.repliers = repliers
        self.name = name

    def get_receiving_type(self):
        """
        Each ``Rule`` defines a :class:`djmessenger.receiving.ReceivingType`,
        this method returns it

        :rtype: ReceivingType
        """
        from djmessenger.receiving import ReceivingType

        try:
            ret = ReceivingType.value_of(self.type)
            return ret
        except KeyError as e:
            logger.error('Given type %s is not a valid receiving type [%s]' %
                         (self.type, ReceivingType.members().keys()))
            raise e

    def get_handler_wrappers(self):
        """

        :return: A list of TargetHandlerClass instances which is a wrapper for
                 BaseHandler
        """
        return getattr(self, 'handlers', [])

    def get_handler_instances(self):
        return [x.get_instance() for x in self.get_handler_wrappers()]

    def get_replier_wrappers(self):
        """

        :return: A list of TargetReplierClass instances which is a wrapper for
                 CommonReplier
        """
        return getattr(self, 'repliers', [])

    def get_replier_instances(self):
        return [x.get_instance() for x in self.get_replier_wrappers()]

    def get_filter_wrappers(self):
        """
        :return: A list of TargetFilterClass instances which is a wrapper for
                 BaseFilter
        """
        return getattr(self, 'filters', [])

    def get_filter_instances(self):
        return [x.get_instance() for x in self.get_filter_wrappers()]

    def __str__(self):
        return '<Rule (%s)>' % getattr(self, 'name', '')

    def __repr__(self):
        return str(self)


class Policy(Serializable):
    """
    A ``Policy`` is the most important component in djmessenger. A Policy
    defines multiple :class:`.Rule` and when we got message from customer, we
    simply :func:`.Policy.apply` the message
    """
    custom_obj_map = {
        'rules': [Rule, list]
    }

    def __init__(self, rules=list()):
        self.rules = rules

    def get_rules(self, rtype):
        ret = []
        for rule in self.rules:
            if rule.get_receiving_type() == rtype:
                ret.append(rule)
        return ret

    @classmethod
    def get_instance(cls, json_data):
        """Given a json string, deserialize it and return a :class:`.Policy`

        :return: Policy
        :rtype: Policy
        """
        try:
            policy = Policy.deserialize(json_data)
            return policy
        except Exception as e:
            logger.error('Failed to load policy file from setting, please '
                         'double check on your settings for DJM_ROUTING_POLICY')

    def get_default_rule(self):
        """
        There can only be 1 Rule that has type DEFAULT, if there were multiple,
        return the first one; return empty list if not found.

        The filters, handlers and repliers defined in DEFAULT Rule will be
        applied on all Rules
        """
        for rule in self.rules:
            if rule.type == ReceivingType.DEFAULT.name:
                return rule
        return Rule('DEFAULT')

    def get_post_message_url(self):
        """

        :return: The Facebook URL to post message
        :rtype: str
        """
        return DJM_POST_MESSAGE_URL

    def get_message_prefix(self, psid=''):
        """
        :param psid: customer's psid
        :type psid: str

        :return: The prefix for each replied message
        :rtype: str
        """
        return DJM_BOT_PREFIX

    def apply(self, messaging):
        """
        Apply this Policy to the given messaging instance

        :param messaging: An instance of Messaging class
        :type messaging: djmessenger.receiving.Messaging
        """
        receiving_type = messaging.get_receiving_type()
        logger.debug('Determined ReceivingType for messaging [%s] as %s'
                     % (messaging, receiving_type))
        rules = self.get_rules(receiving_type)
        logger.debug('Successfully fetched rules to be applied on [%s] as %s'
                     % (messaging, rules))
        default_rule = self.get_default_rule()
        for rule in rules:
            logger.debug('Applying rule %s on %s' % (rule, messaging))
            # apply filters
            any_filter_failed = False
            for filter_ in rule.get_filter_instances() + default_rule.get_filter_instances():
                logger.debug('Applying filter %s from rule %s on %s'
                             % (filter_, rule, messaging))
                if not filter_.should_pass(messaging):
                    logger.debug('Given messaging [%s] did not pass filter %s, '
                                 'skipping Rule %s' % (messaging, filter_, rule))
                    any_filter_failed = True
                    break
            if any_filter_failed:
                continue
            logger.debug('Successfully applied all filters, proceed with '
                         'handlers')
            # filters passed, apply handlers
            for handler in rule.get_handler_instances() + default_rule.get_handler_instances():
                logger.debug('Applying handler %s from rule %s on %s'
                             % (handler, rule, messaging))
                handler.handle(messaging)
            logger.debug('Successfully applied all handlers, proceed with '
                         'repliers')
            # handlers processed, apply repliers
            for replier in rule.get_replier_instances() + default_rule.get_replier_instances():
                logger.debug('Applying replier %s from rule %s on %s'
                             % (replier, rule, messaging))
                replier.reply(messaging,
                              self.get_post_message_url(),
                              self.get_message_prefix(messaging.get_psid()))
            logger.debug('Successfully applied rule %s on %s' % (rule,
                                                                 messaging))
        logger.debug('Successfully applied all rules on %s' % messaging)
