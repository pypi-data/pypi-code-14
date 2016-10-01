# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool

from party import Address
from carrier import Carrier, CarrierService, BoxType
from sale import Configuration, Sale
from stock import ShipmentOut


def register():
    Pool.register(
        Address,
        Carrier,
        CarrierService,
        BoxType,
        Configuration,
        Sale,
        ShipmentOut,
        module='shipping_fedex', type_='model'
    )
