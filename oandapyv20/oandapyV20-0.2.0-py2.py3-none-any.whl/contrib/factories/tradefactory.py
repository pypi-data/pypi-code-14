# -*- coding: utf-8 -*-
import sys
from oandapyV20.contrib.requests import TradeCloseRequest
import oandapyV20.endpoints.trades as trades


def trade_request_factory(accountID, factoryType, **kwargs):
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
    # get the creator for the 'product' we want from factory factoryType
    creator = getattr(sys.modules[__name__], factoryType)

    d = kwargs
    tradeID = d['tradeID']
    del d['tradeID']

    try:
        # create the 'product' to fabricate
        f = creator(**d)
    except Exception as e:
        raise e
    else:
        # process the 'product' by creating the API-request with order data
        if factoryType in ['TradeCloseRequest']:
            return trades.TradeClose(accountID,
                                     tradeID=tradeID,
                                     data=f.data)
