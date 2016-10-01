# -*- coding: utf-8 -*-
"""
    tests/conftest.py

"""
import os
import time

import pytest
from trytond.modules.fulfilio.tests.conftest import *  # noqa
from trytond.pool import Pool
from trytond.config import config
config.set('database', 'path', '/tmp/tryton-test-db/')
if not os.path.exists(config.get('database', 'path')):
    os.makedirs(config.get('database', 'path'))


def pytest_addoption(parser):
    parser.addoption(
        "--db", action="store", default="sqlite",
        help="Run on database: sqlite or postgres"
    )
    parser.addoption(
        "--reuse-db", action="store_true", default=False,
        help="Reuse the previously created database"
    )
    parser.addoption(
        "--reset-db", action="store_true", default=False,
        help="Clear local database and initialise"
    )


@pytest.fixture(scope='session', autouse=True)
def install_module(request):
    """
    Install tryton module in specified database.
    """
    reuse_db = request.config.getoption("--reuse-db")

    if request.config.getoption("--db") == 'sqlite':
        os.environ['TRYTOND_DATABASE_URI'] = "sqlite://"
        if reuse_db:
            # A hack to check if the database exists and if it
            # does, load that and run tests.
            Database = backend.get('Database')

            # cursor.test forgets to set flavor!
            # no time to report a bug!
            Flavor.set(Database.flavor)
            os.environ['DB_NAME'] = 'fulfilio'
        else:
            os.environ['DB_NAME'] = ':memory:'

    elif request.config.getoption("--db") == 'postgres':
        os.environ['TRYTOND_DATABASE_URI'] = "postgresql://"
        if reuse_db:
            os.environ['DB_NAME'] = 'test_fulfilio'
        else:
            os.environ['DB_NAME'] = 'test_' + str(int(time.time()))

    if reuse_db:
        Database = backend.get('Database')
        database = Database().connect()
        cursor = database.cursor()
        databases = database.list(cursor)
        cursor.close()
        if os.environ['DB_NAME'] in databases:
            if request.config.getoption("--reset-db"):
                cursor = database.cursor()
                databases = database.drop(cursor, os.environ['DB_NAME'])
                cursor.close()
            else:
                # tryton test forgets to init the Pool
                # for existing database
                Pool(os.environ['DB_NAME']).init()

    config.set('database', 'uri', os.environ['TRYTOND_DATABASE_URI'])
    from trytond.tests import test_tryton
    test_tryton.install_module('fulfilio')
    test_tryton.install_module('shipping_fedex')


@pytest.fixture
def john_doe(usa, us_fl):
    Party = Pool().get('party.party')

    customer, = Party.create([{
        'name': 'John Doe',
        'addresses': [('create', [{
            'name': 'John Doe',
            'street': '250 NE 25th St',
            'zip': '33127',
            'city': 'Miami, Miami-Dade',
            'country': usa.id,
            'subdivision': us_fl.id,
        }])],
        'contact_mechanisms': [('create', [{
            'type': 'phone',
            'value': '123456789'
        }])]
    }])
    return customer


@pytest.fixture
def fedex_carrier(usd, carrier_product):
    Party = Pool().get('party.party')
    Carrier = Pool().get('carrier')
    SaleConfiguration = Pool().get('sale.configuration')
    ModelData = Pool().get('ir.model.data')
    SaleReturnPolicy = Pool().get('sale.return.policy')
    BoxType = Pool().get('carrier.box_type')
    Service = Pool().get('carrier.service')

    # Create carrier
    carrier_party, = Party.create([{
        'name': 'FedEx',
    }])

    fedex_carrier, = Carrier.create([{
        'party': carrier_party.id,
        'carrier_product': carrier_product.id,
        'currency': usd.id,
        'carrier_cost_method': 'fedex',
        'fedex_key': 'w8B7YBVgtfnDgn0k',
        'fedex_account_number': '510088000',
        'fedex_password': 'blDSZptRcXwqg3VTSJcU9xNbc',
        'fedex_meter_number': '118518591',
        'fedex_is_test': True,
        'services': [(
            'add', Service.search([('carrier_cost_method', '=', 'fedex')])
        )],
        'box_types': [(
            'add', BoxType.search([('carrier_cost_method', '=', 'fedex')])
        )]
    }])

    return_policy, = SaleReturnPolicy.create([{'name': 'default_policy'}])

    sale_config = SaleConfiguration(1)
    sale_config.fedex_box_type = \
        ModelData.get_id('shipping_fedex', 'packaging_fedex_box')
    sale_config.fedex_carrier_service = \
        ModelData.get_id('shipping_fedex', 'service_fedex_2_day')
    sale_config.default_return_policy = return_policy
    sale_config.round_down_account = 4  # cash account
    sale_config.save()

    return fedex_carrier
