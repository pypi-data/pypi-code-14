# -*- coding: utf-8 -*-
from shop.signals import cart_user_changed
from shop.globals import current_cart


def copy_flipgive_id(sender):
    "Copy flipgive_token to created party"
    cart = current_cart
    # Save FlipGive Token to Party if available in Cart
    if cart.flipgive_token:
        party = cart.sale.party
        party.flipgive_token = cart.flipgive_token
        party.save()

    # Save FlipGive instance to Sale if available in Cart
    if cart.flipgive_campaign:
        sale = cart.sale
        sale.flipgive_campaign = cart.flipgive_campaign.id
        sale.save()


def register_signals(app):
    "Registers signals with app"
    cart_user_changed.connect(copy_flipgive_id, app)
