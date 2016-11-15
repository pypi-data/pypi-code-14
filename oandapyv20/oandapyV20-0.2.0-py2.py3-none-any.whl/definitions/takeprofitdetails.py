# -*- coding: utf-8 -*-
"""Transactions definitions."""
from oandapyV20.definitions.orders import TimeInForce, OrderType
from oandapyV20.contrib.requests.baserequest import BaseRequest

class TakeProfitDetails(BaseRequest):

    def __init__(self,
                 price,
                 timeInForce=TimeInForce.GTC,
                 gtdTime=None,
                 clientExtensions=None):
        """Instantiate TakeProfitDetails.
      
        This is a representation of the specification for a TakeProfitOrder. 
        """
        super(TakeProfitDetails, self).__init__()
        self._data.update({"type": OrderType.TAKE_PROFIT})

        if timeInForce not in [TimeInForce.GTC,
                               TimeInForce.GTD,
                               TimeInForce.GFD]:
            raise ValueError("timeInForce: {}".format(timeInForce))

        self._data.update({"timeInForce": timeInForce})

        # optional, but required if
        if timeInForce == TimeInForce.GTD and not gtdTime:
            raise ValueError("gtdTime: value required when timeInForce is GTD")
        self._data.update({"gtdTime": gtdTime})
