# -*- coding: utf-8 -*-
import sys

from oandapyV20.contrib.requests import PositionCloseRequest
import oandapyV20.endpoints.positions as positions


def get_creator(name, factoryType):
    # get the creator for the 'product' we want from factory factoryType
    try:
        # print("get_creator: ", name, factoryType)
        creator = getattr(sys.modules[name], factoryType)
    except Exception as e:
        raise ValueError("No 'creator' for {}".format(factoryType))
    else:
        return creator


def position_request_factory(accountID, factoryType, **kwargs):
    r"""create a position request based on the factoryType.

    The factoryType represents one of the known ordertype classes.
    This class is used as 'creator' to create the 'order' which is
    then passed as data to create the endpoint request.

    Parameters
    ----------
    factoryType : string (required)
        one of the known ordertype classes.

    \*\*kwargs : parameters (required)
        parameters corresponding with the parameters of the specified
        factoryType.

    """
    # no arguments for these
    if factoryType in ['PositionListRequest']:
        return positions.PositionList(accountID)
    elif factoryType in ['OpenPositionsRequest']:
        return positions.OpenPositions(accountID)

    instrument = None
    d = None
    try:
        instrument = kwargs['instrument']
    except Exception as e:
        raise ValueError("instrument missing")
    else:
        d = kwargs
        del d['instrument']

    # process the 'product' by creating the API-request with request data
    if factoryType == 'PositionCloseRequest':
        # create the 'product'
        creator = get_creator(__name__, factoryType)
        f = creator(**d)

        return positions.PositionClose(accountID,
                                       instrument=instrument,
                                       data=f.data)

    elif factoryType == 'PositionDetailsRequest':
        return positions.PositionDetails(accountID,
                                         instrument=instrument)
