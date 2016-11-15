# -*- coding: utf-8 -*-
"""order factory.

higher level interface to create orders.


    api = oandapyV20.API(access_token=access_token)

    mor = request_factory(accountID, "MarketOrderRequest",
                          instrument="EUR_USD", unit=100)

    rv = api.request(mor)
    print(json.dumps(rv, indent=2))

    acr = request_factory(accountID, "AccountConfiguration",
                          alias="hootnotv20", margin=0.1)

CancelAll
"""
import sys
from oandapyV20.contrib.requests import (
    MarketOrderRequest,
    LimitOrderRequest)
import oandapyV20.endpoints.orders as orders


def order_request_factory(accountID, factoryType, **kwargs):
    r"""create an order request based on the factoryType.

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
    # straight
    if factoryType in ['CancelOrderRequest']:
        return orders.OrderCancel(accountID, orderID=kwargs['orderID'])

    # get the creator for the 'product' we want from factory factoryType
    creator = getattr(sys.modules[__name__], factoryType)
    try:
        # create the 'product'
        f = creator(**kwargs)
    except Exception as e:
        raise e
    else:
        # process the 'product' by creating the API-request with order data
        if factoryType in ['MarketOrderRequest', 'LimitOrderRequest']:
            return orders.OrderCreate(accountID, data=f.data)
