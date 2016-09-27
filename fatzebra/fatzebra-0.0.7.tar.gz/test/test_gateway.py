# -*- coding: utf-8 -*-
import datetime
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import fatzebra

# Setup some test details
VALID_CARD = '5123456789012346'
DECLINED_CARD = '4242424242424242'
INVALID_CARD = '5123456789012345'

NOW = datetime.datetime.now()
VALID_EXPIRY = "%d/%d" % (NOW.month, NOW.year + 4)

class FatZebraTestCase(unittest.TestCase):
    def setUp(self):
        super(FatZebraTestCase, self).setUp()

class FatZebraGatewayTest(FatZebraTestCase):
    def test_gateway_sets_parameters_properly(self):
        gateway = fatzebra.gateway.Gateway("Franks", "Beans")
        self.assertEqual(gateway.username, "Franks")
        self.assertEqual(gateway.token, "Beans")

    def test_uri_is_built_properly(self):
        gateway = fatzebra.gateway.Gateway("TEST", "TEST", False)
        self.assertEqual(
            gateway._uri(), "https://gateway.fatzebra.com.au/v1.0/purchases")

    def test_purchase_works(self):
        gw = fatzebra.gateway.Gateway()
        result = gw.purchase(
            100,
            "pytest-" + str(random.random()),
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(result.successful)

    def test_successful_query(self):
        gw = fatzebra.gateway.Gateway()
        ref = "pytest-" + str(random.random())
        result = gw.purchase(
            100,
            ref,
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(result.successful)
        query = gw.query(result.id)
        self.assertTrue(result.successful)
        self.assertEqual(result.reference,ref)

    def test_failed_query(self):
        gw = fatzebra.gateway.Gateway()
        ref = "pytest-" + str(random.random())
        result = gw.purchase(
            151, # Amount ending in 51 etc will return error.
            ref,
            "Test Card",
            DECLINED_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertFalse(result.successful)
        query = gw.query(result.id)
        self.assertEqual(result.reference,ref)

    def test_purchase_with_invalid_card_responds_properly(self):
        gw = fatzebra.gateway.Gateway()
        result = gw.purchase(
            151, # Amount ending in 51 etc will return error.
            "pytest-" + str(random.random()),
            "Test Card",
            DECLINED_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertFalse(result.successful)

    def test_errors_are_handled_properly(self):
        gw = fatzebra.gateway.Gateway()
        with self.assertRaises(fatzebra.errors.GatewayError):
            result = gw.purchase(
                100,
                "pytest-" + str(random.random()),
                "Test Card",
                INVALID_CARD,
                VALID_EXPIRY,
                "123",
                "1.2.3.4")

    def test_tokenize(self):
        gw = fatzebra.gateway.Gateway()
        result = gw.tokenize("Jim Murphy", VALID_CARD, VALID_EXPIRY, "123")
        self.assertIsNotNone(result.token)

    def test_token_purchase(self):
        gw = fatzebra.gateway.Gateway()
        card = gw.tokenize("Jim Murphy", VALID_CARD, VALID_EXPIRY, "123")
        result = gw.purchase_with_token(
            100, "pytoken" + str(random.random()), card.token, None, "1.2.3.4")
        self.assertTrue(result.successful)

    def test_invalid_token_purchase(self):
        gw = fatzebra.gateway.Gateway()
        with self.assertRaises(fatzebra.errors.GatewayUnknownResponseError):
            result = gw.purchase_with_token(
                100, "pytoken" + str(random.random()), "abc123", None,
                "1.2.3.4")

    def test_authentication_error(self):
        gw = fatzebra.gateway.Gateway("INVALID", "USER")
        with self.assertRaises(fatzebra.errors.AuthenticationError):
            gw.tokenize("Jim Smith", VALID_CARD, VALID_EXPIRY, "123")

    def test_refund(self):
        gw = fatzebra.gateway.Gateway()
        purchase = gw.purchase(
            100,
            "pytest-" + str(random.random()),
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(purchase.successful)

        response = gw.refund(
            purchase.id,
            purchase.amount,
            "pyrefundtest" + str(random.random())
        )
        self.assertTrue(response.successful)

    def test_unmatched_refund(self):
        gw = fatzebra.gateway.Gateway()
        response = gw.unmatched_refund(
            100,
            "pytest-" + str(random.random()),
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(response.successful)

if __name__ == '__main__':
    unittest.main()
