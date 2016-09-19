#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
The client
"""

# Python
from __future__ import unicode_literals
from datetime import datetime
import re
import os

# Third-party 
import requests
import pytz
from bs4 import BeautifulSoup
from lxml import etree

# Project
from fnapy.connection import FnapyConnection
from fnapy.fnapy_manager import FnapyManager
from fnapy.utils import get_order_ids, Message


# FUNCTIONS
def hide_credentials(text):
    """@todo: Docstring for hide_credentials.
    :returns: @todo

    """
    credentials = ('partner_id', 'shop_id', 'token')
    hidden = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    for credential in credentials:
        text = re.sub(pattern=' {}="[^"]+"'.format(credential),
                  repl=' {0}="{1}"'.format(credential, hidden),
                  string=text, flags=0)
    return text


def save_xml_assets(service, xml_request, xml_response):
    """Save the raw XML in a file"""
    # Request
    output_filename = 'tests/assets/' + service + '.xml'
    with open(output_filename, 'w') as f:
        f.write(hide_credentials(xml_request).encode('utf-8'))
    print 'Saved the XML request to {}'.format(output_filename)

    # Response
    output_filename = 'tests/assets/' + service + '_response.xml'
    with open(output_filename, 'w') as f:
        f.write(xml_response.xml.encode('utf-8'))
    print 'Saved the XML response to {}'.format(output_filename)

# INPUTS
partner_id = os.environ.get('FNAC_PARTNER_ID')
shop_id    = os.environ.get('FNAC_SHOP_ID')
key        = os.environ.get('FNAC_KEY')

ACTIVE_SERVICES = {}
ACTIVE_SERVICES['auth']                         = True
ACTIVE_SERVICES['offers_update']                = False
ACTIVE_SERVICES['batch_status']                 = False
ACTIVE_SERVICES['offers_query']                 = True
ACTIVE_SERVICES['orders_query']                 = False
ACTIVE_SERVICES['orders_update']                = False
ACTIVE_SERVICES['pricing_query']                = False
ACTIVE_SERVICES['carriers_query']               = False
ACTIVE_SERVICES['client_order_comments_query']  = False
ACTIVE_SERVICES['client_order_comments_update'] = False
ACTIVE_SERVICES['messages_query']               = False
ACTIVE_SERVICES['messages_update']              = False
ACTIVE_SERVICES['incidents_query']              = False
ACTIVE_SERVICES['incidents_update']             = False
ACTIVE_SERVICES['shop_invoices_query']          = False


# PROCESSING

# Get a token 
# Service: auth
conn = FnapyConnection(partner_id, shop_id, key)

manager = FnapyManager(conn)

if ACTIVE_SERVICES['auth']:
    print "Authenticating..."
    token = manager.authenticate()


# Update offers
# Service: offers_update
if ACTIVE_SERVICES['offers_update']:
    offer_data1 = {'product_reference':'0711719247159',
            'offer_reference':'B76A-CD5-153',
            'price':15, 'product_state':11, 'quantity':10, 
            'description': 'New product - 2-3 days shipping, from France'}

    offer_data2 = {'product_reference':'5030917077418',
            'offer_reference':'B067-F0D-75E',
            'price':20, 'product_state':11, 'quantity':16, 
            'description': 'New product - 2-3 days shipping, from France'}

    # SICP
    offer_data3 = {'product_reference':'9780262510875',
            'offer_reference':'B76A-CD5-444',
            'price':80, 'product_state':11, 'quantity':10, 
            'description': 'New product - 2-3 days shipping, from France'}

    # Batman V Superman L'aube de la justice 
    offer_data4 = {'product_reference':'5051889562672',
            'offer_reference':'B067-F0D-444',
            'price':20, 'product_state':11, 'quantity':16, 
            'description': 'New product - 2-3 days shipping, from France'}

    offers_data = [offer_data1, offer_data2, offer_data3, offer_data4]
    print "Updating offers..."
    offers_update_response = manager.update_offers(offers_data)
    save_xml_assets('offers_update', manager.offers_update_request, offers_update_response)


# Get the status of the last operation
# Service: batch status
if ACTIVE_SERVICES['batch_status']:
    print "Getting batch status..."
    batch_id = offers_update_response.dict.get('offers_update_response', {}).get('batch_id')
    batch_status_response = manager.get_batch_status(batch_id)
    save_xml_assets('batch_status', manager.batch_status_request, batch_status_response)


# Query the offers
# Service: offers_query
if ACTIVE_SERVICES['offers_query']:
    # Between 2 datetimes
    dmin = datetime(2016, 8, 23, 0, 0, 0).replace(tzinfo=pytz.utc)
    dmax = datetime(2016, 9, 2, 0, 0, 0).replace(tzinfo=pytz.utc)
    print "Querying offers between {dmin} and {dmax}...".format(dmin=dmin.isoformat(), dmax=dmax.isoformat())
    date = {'@type': 'Modified',
    'min': {'#text': dmin.isoformat()},
    'max': {'#text': dmax.isoformat()}
    }

    # Within the given page
    quantity = {'@mode': 'Equals', '@value': 16}
    offers_query_response = manager.query_offers(quantity=quantity)
    save_xml_assets('offers_query', manager.offers_query_request, offers_query_response)

# Query orders
# Service: orders_query
if ACTIVE_SERVICES['orders_query']:
    orders_query_response = manager.query_orders(results_count=10, paging=1)
    order_ids = get_order_ids(orders_query_response)
    save_xml_assets('orders_query', manager.orders_query_request, orders_query_response)


# # Update orders
# # Service: orders_update
if ACTIVE_SERVICES['orders_update']:
    action1 = {"order_detail_id": 1, "action": "Accepted"}
    action2 = {"order_detail_id": 2, "action": "Refused"}
    actions = [action1, action2]
    orders_update_response = manager.update_orders(order_ids[0], "accept_order", actions)
    save_xml_assets('orders_update', manager.orders_update_request,
                    orders_update_response)


# Query pricing
# Service: pricing_query
if ACTIVE_SERVICES['pricing_query']:
    print "Querying the pricing..."
    pricing_query_response = manager.query_pricing("0886971942323")
    save_xml_assets('pricing_query', manager.pricing_query_request,
                    pricing_query_response)


# # Query carrier
# # Service: carriers_query
if ACTIVE_SERVICES['carriers_query']:
    carriers_query_response = manager.query_carriers()
    save_xml_assets('carriers_query', manager.carriers_query_request,
                    carriers_query_response)


# Query client order comments
# Service: client_order_comments_query
if ACTIVE_SERVICES['client_order_comments_query']:
    client_order_comments_query_response = manager.query_client_order_comments(rate={'@mode': 'Equals', '@value': '1'})
    save_xml_assets('client_order_comments_query',
                    manager.client_order_comments_query_request, client_order_comments_query_response)


# Update client order comments
# Service: client_order_comments_update
if ACTIVE_SERVICES['client_order_comments_update']:
    client_order_comments_update_response = manager.update_client_order_comments('Hello', '8D7472DB-7EAF-CE05-A960-FC12B812FA14')
    save_xml_assets('client_order_comments_update',
                    manager.client_order_comments_update_request, client_order_comments_update_response)


# Query messages
# Service: messages_query
if ACTIVE_SERVICES['messages_query']:
    messages_query_response = manager.query_messages(paging='1')
    save_xml_assets('messages_query', manager.messages_query_request, messages_query_response)


# Update messages
# Service: messages_update
if ACTIVE_SERVICES['messages_update']:
    message1 = Message(action='mark_as_read', id=u'6F9EF013-6387-F433-C3F5-4AAEF32AA317')
    message1.subject = 'order_information'
    messages_update_response = manager.update_messages([message1])
    save_xml_assets('messages_update', manager.messages_update_request, messages_update_response)


# Query incidents
# Service: incidents_query
if ACTIVE_SERVICES['incidents_query']:
    incidents_query_response = manager.query_incidents(paging=1)
    save_xml_assets('incidents_query', manager.incidents_query_request, incidents_query_response)


# Update incidents
# Service: incidents_update
if ACTIVE_SERVICES['incidents_update']:
    reasons = [{"order_detail_id": 2, "refund_reason": 'no_stock'}]
    incidents_update_response = manager.update_incidents(u'57BEAFDA828A8',
                                                              'refund',  reasons)
    save_xml_assets('incidents_update', manager.incidents_update_request, incidents_update_response)


# Query shop invoices
# Service: shop_invoices_query
if ACTIVE_SERVICES['shop_invoices_query']:
    shop_invoices_query_response = manager.query_shop_invoices(paging=1)
    save_xml_assets('shop_invoices_query', manager.shop_invoices_query_request, shop_invoices_query_response)
