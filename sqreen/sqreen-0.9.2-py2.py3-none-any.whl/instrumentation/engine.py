# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Instrumentation helper responsible for adding dynamic callback
"""
import sys
import logging

from .strategies import SetAttrStrategy, DBApi2Strategy, ImportHookStrategy
from .strategies import DjangoStrategy, Psycopg2Strategy, FlaskStrategy

from ..remote_exception import RemoteException


LOGGER = logging.getLogger(__name__)


class Instrumentation(object):
    """ The instrumentation class is the exposed face of the
    instrumentation engine. It dispatchs to the right strategy,
    the default one is set_attr.

    The instrumentation class takes a channel as parameter. The channel
    is a callable accepting 1 parameter where events, attacks and
    remote exception will be sent to. It can be CappedQueue.push or simply
    list().append

    The instrument class dispatch to different strategies based on strategy
    name defined in callback. It ask stategy for an unique id based on hook path
    infos and ensure to have only one strategy instance per id. It's needed
    for DBApi2 strategy where every sqlite3 callbacks will be stored in the same
    strategy to avoid double-instrumentation.
    """

    def __init__(self, channel, before_hook_point=None):
        self.channel = channel
        self.strategies = {}
        self.before_hook_point = before_hook_point

    def add_callback(self, callback):
        """ Add a callback. The callback defines itself where it should
        hook to and the strategy use for hooking (set_attr or DBApi2)
        """
        try:
            strategy_class = self._get_strategy_class(callback.strategy)

            # Get the strategy id
            strategy_id = strategy_class.get_strategy_id(callback)

            # Check if we already have a strategy
            if strategy_id in self.strategies:
                strategy_instance = self.strategies[strategy_id]
                LOGGER.debug("Reusing strategy %s for id %s",
                             strategy_instance, strategy_id)
            else:
                strategy_instance = strategy_class(strategy_id, self.channel,
                                                   self.before_hook_point)
                LOGGER.debug("Instantiate strategy %s for id %s -> %s",
                             strategy_class, strategy_id, strategy_instance)
                self.strategies[strategy_id] = strategy_instance

            strategy_instance.hook(callback)
        except Exception:
            # If the strategy fails to hook either at instantiation
            # or hook method, catch the exception and log it
            LOGGER.exception("Callback %r fails to hook", callback, exc_info=True)

            # And send the exception back to the backend
            infos = {'callback': callback.__dict__}
            remote_exception = RemoteException(sys.exc_info(), infos)
            self.channel(remote_exception)

    def deinstrument(self, callback):
        """ Deactive instrumentation on the callback endpoint
        """
        strategy_class = self._get_strategy_class(callback.strategy)

        # Get the strategy id
        strategy_id = strategy_class.get_strategy_id(callback)

        self.strategies[strategy_id].deinstrument(callback)

    def deinstrument_all(self):
        """ Deactive instrumentation on all callbacks by calling
        deinstrument_all on all strategies
        """
        for strategy in self.strategies.values():
            strategy.deinstrument_all()

    @staticmethod
    def _get_strategy_class(strategy):
        """ Return a strategy class depending on the strategy name passed
        in parameter.
        Raise a NotImplementedError if the strategy is unknown.
        """
        if strategy == 'set_attr':
            return SetAttrStrategy
        elif strategy == 'import_hook':
            return ImportHookStrategy
        elif strategy == 'DBApi2':
            return DBApi2Strategy
        elif strategy == 'django':
            return DjangoStrategy
        elif strategy == 'psycopg2':
            return Psycopg2Strategy
        elif strategy == 'flask':
            return FlaskStrategy
        else:
            err_msg = "Unknown hooking_strategy {}"
            raise NotImplementedError(err_msg.format(strategy))
