# -*- coding: utf-8 -*-
"""
    tests/test_view_depends.py
    :copyright: (C) 2016 by Fulfil.IO Inc.
    :license: see LICENSE for more details.
"""


class TestViewsDepends:
    '''
    Test views and depends
    '''

    def test_views(self):
        "Test Views"
        from trytond.transaction import Transaction
        from trytond.tests.test_tryton import USER, CONTEXT, DB_NAME
        from trytond.tests.test_tryton import test_view
        Transaction().cursor.rollback()
        Transaction().stop()

        test_view('shipping_fedex')

        Transaction().start(DB_NAME, USER, context=CONTEXT)

    def test_depends(self):
        "Test depends"
        from trytond.transaction import Transaction
        from trytond.tests.test_tryton import USER, CONTEXT, DB_NAME
        from trytond.tests.test_tryton import test_depends
        Transaction().cursor.rollback()
        Transaction().stop()

        test_depends()

        Transaction().start(DB_NAME, USER, context=CONTEXT)
