# -*- coding: utf-8 -*-
"""request factory.

higher level interface to create API-requests.


    api = oandapyV20.API(access_token=access_token)

    mor = request_factory(accountID, "MarketOrderRequest",
                          instrument="EUR_USD", unit=100)

    rv = api.request(mor)
    print(json.dumps(rv, indent=2))
"""
import sys
import re
import importlib
from .orderfactory import order_request_factory
from .positionfactory import position_request_factory
from .tradefactory import trade_request_factory
from oandapyV20.contrib.requests import *

def _request_factory(accountID, factoryType, **kwargs):
    r"""create a request based on the factoryType.

    The request_factory serves as a wrapper for the different
    request factories serving their specific requests.

    Parameters
    ----------
    factoryType : string (required)
        one of the known ordertype classes.

    \*\*kwargs : parameters (required)
        parameters corresponding with the parameters of the specified
        factoryType.
    """
    if "Order" in factoryType:
        return order_request_factory(accountID, factoryType, **kwargs)

    if "Position" in factoryType:
        return position_request_factory(accountID, factoryType, **kwargs)

    if "Trade" in factoryType:
        return trade_request_factory(accountID, factoryType, **kwargs)

    # we should never get here
    raise TypeError("No factory for {}".format(factoryType))


def get_creator(name, factoryType):
    # get the creator for the 'product' we want from factory factoryType
    try:
        # print("get_creator: ", name, factoryType)
        creator = getattr(sys.modules[name], factoryType)
    except Exception as e:
        raise ValueError("No 'creator' for {}".format(factoryType))
    else:
        return creator

def request_factory(accountID, factoryType, **kwargs):
    """ """
    creator = getattr(sys.modules[__name__], factoryType)
    return creator
#
#def position_request_factory(accountID, factoryType, **kwargs):
#    r"""create a position request based on the factoryType.
#
#    The factoryType represents one of the known ordertype classes.
#    This class is used as 'creator' to create the 'order' which is
#    then passed as data to create the endpoint request.
#
#    Parameters
#    ----------
#    factoryType : string (required)
#        one of the known ordertype classes.
#
#    \*\*kwargs : parameters (required)
#        parameters corresponding with the parameters of the specified
#        factoryType.
#
#    """
#    # no arguments for these
#    if factoryType in ['PositionListRequest']:
#        return positions.PositionList(accountID)
#    elif factoryType in ['OpenPositionsRequest']:
#        return positions.OpenPositions(accountID)
#
#    instrument = None
#    d = None
#    try:
#        instrument = kwargs['instrument']
#    except Exception as e:
#        raise ValueError("instrument missing")
#    else:
#        d = kwargs
#        del d['instrument']
#
#    # process the 'product' by creating the API-request with request data
#    if factoryType == 'PositionCloseRequest':
#        # create the 'product'
#        creator = get_creator(__name__, factoryType)
#        f = creator(**d)
#
#        return positions.PositionClose(accountID,
#                                       instrument=instrument,
#                                       data=f.data)
#
#    elif factoryType == 'PositionDetailsRequest':
#        return positions.PositionDetails(accountID,
#                                         instrument=instrument)
