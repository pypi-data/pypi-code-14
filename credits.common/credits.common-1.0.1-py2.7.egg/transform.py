#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook

from credits.interface import Hashable
from credits.interface import Marshallable


class Transform(Marshallable, Hashable):
    def __init__(self):
        self.logger = logbook.Logger(__name__)

    def verify(self, state):
        """
        Verify that this transform is still applicable in the future. Raise an exception if it can't verify.

        :param state: The state to verify against.
        :type: credits.state.State
        :return: bool
        """
        raise NotImplementedError()

    def apply(self, state):
        """
        Perform last minute checks that the transform can specifically apply _now_. Then apply. Return the new state.

        :param state: The state to apply against.
        :type: credits.state.State
        :return: credits.state.State
        """
        raise NotImplementedError()

    def required_authorizations(self):
        """
        Return a list of address's that must provide a proof for the parent transaction apply correctly.

        :return:
        """
        return []

    def get_challenge(self, hash_provider):
        raise NotImplementedError()
