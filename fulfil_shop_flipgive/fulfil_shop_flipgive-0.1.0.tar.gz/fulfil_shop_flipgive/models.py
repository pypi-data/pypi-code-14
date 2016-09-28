# -*- coding: utf-8 -*-
"""Flipgive models"""
from fulfil_client.model import (ModelType, StringType)

import shop.cart.models
import shop.user.models
from shop.fulfilio import Model


class Sale(shop.cart.models.Sale):
    flipgive_campaign = ModelType("flipgive.campaign")

shop.cart.models.Sale = Sale


class Cart(shop.cart.models.Cart):
    flipgive_campaign = ModelType("flipgive.campaign")
    flipgive_token = StringType()

shop.cart.models.Cart = Cart


class Party(shop.user.models.Party):
    # XXX: FlipGive Token is saved on Party because it can be used for
    # shopping multiple times (especially phone order). Token can be
    # reused only for the campaign it is associated to. In case, the
    # user comes from different FlipGive Campaign, this token should
    # be updated.
    flipgive_token = StringType()

shop.user.models.Party = Party


class FlipGiveCampaign(Model):
    __model_name__ = 'flipgive.campaign'

    name = StringType()
    campaign_id = StringType()
