# -*- coding: utf-8 -*-
"""Handle forexlabs endpoints."""
from .apirequest import APIRequest
from .decorators import dyndoc_insert, endpoint
from .definitions.forexlabs import definitions    # flake8: noqa
from .responses.forexlabs import responses
from abc import abstractmethod


class Forexlabs(APIRequest):
    """Forexlabs - abstract baseclass to handle Forexlabs endpoint."""

    ENDPOINT = ""
    METHOD = "GET"

    @dyndoc_insert(responses)
    def __init__(self, instrument=None):
        """Instantiate a Forexlabs APIRequest instance.

        Parameters
        ----------
        instrument : string (optional)
            the instrument to fetch candle data for
        """
        endpoint = self.ENDPOINT.format(instrument=instrument)
        super(Forexlabs, self).__init__(endpoint, method=self.METHOD)


@endpoint("v3/labs/{instrument}/calendar")
class ForexlabsCalendar(ForexLabs):
    """Get economic calendar information."""

    def __init__(self, period, instrument=None, params=None):
        """some docs."""
        super(ForexlabsCalendar, self).__init__()
        self.params = params


@endpoint("v3/labs/{instrument}/ratios")
class ForexlabsPositionRations(ForexLabs):
    """Forexlabs Historical Position Ratios."""

    def __init__(self, period, instrument=None, params=None):
        """some docs."""
        super(ForexlabsCalendar, self).__init__()
        self.params = params


@endpoint("v3/labs/{instrument}/spreads")
class ForexlabsSpreads(ForexLabs):
    """Get Spread Information for instrument."""

    def __init__(self, period, instrument=None, params=None):
        """some docs."""
        super(ForexlabsCalendar, self).__init__()
        self.params = params
