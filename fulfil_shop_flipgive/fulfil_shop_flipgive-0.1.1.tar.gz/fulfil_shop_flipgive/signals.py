# -*- coding: utf-8 -*-
from shop.signals import cart_user_changed
from shop.globals import current_cart


def copy_flipgive_id(sender):
    "Copy flipgive_campaign to created party"
    cart = current_cart
    # Save FlipGive Campaign to sale and party if available in Cart
    if cart.flipgive_campaign and cart.sale:
        sale = cart.sale
        sale.flipgive_campaign = cart.flipgive_campaign.id
        sale.save()

        party = cart.sale.party
        party.flipgive_campaign = cart.flipgive_campaign.id
        party.save()


def register_signals(app):
    "Registers signals with app"
    cart_user_changed.connect(copy_flipgive_id, app)
