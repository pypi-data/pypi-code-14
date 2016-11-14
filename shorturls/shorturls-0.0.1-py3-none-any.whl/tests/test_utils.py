# -*- coding: utf-8 -*-

from django.test.client import RequestFactory
from django.test.testcases import TestCase

from shorturls.utils.shortcuts import get_shorturl
from shorturls.utils.nonce import NonceFactory


class NonceFactoryTests(TestCase):

    def test_encode_decode(self):
        """
        Tests that the core base-N encoding workds
        """
        nonce_factory = NonceFactory()
        for n in range(0,100000):
            encoded = nonce_factory.base_encode(n)
            decoded = nonce_factory.base_decode(encoded)
            self.assertEqual(n, decoded)

    def test_get_alphabet(self):
        alphabet = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        nonce_factory = NonceFactory(alphabet=alphabet)
        self.assertEqual(nonce_factory.get_alphabet(), alphabet)

    def test_get_nonce_of_bits(self):
        """
        Test that get_nonce_of_bits() works.
        """
        nonce_factory = NonceFactory()
        entropy_map = [
            (6, 33), (8, 44), (12, 67), (16, 89),
            (20, 111), (23, 128), (24, 134), ]
        for chars, bits in entropy_map:
            nonce = nonce_factory.get_nonce_of_bits(bits)
            self.assertTrue(len(nonce) <= chars)

    def test_get_nonce_randomness(self):
        """
        Tests that get_nonce() doesn't produce duplicate nonces.
        """
        nonce_factory = NonceFactory()
        nonces = set()
        for n in range(0, 10000):
            nonce = nonce_factory.get_nonce(chars=8)
            nonces.add(nonce)

        self.assertEqual(len(nonces), 10000,
                         'get_nonce() produced identical nonces')

    def test_get_nonce_chars(self):
        """
        Tests that get_nonce() can be used to create nonces with
        specific lengths.
        """
        nonce_factory = NonceFactory()
        for n in range(8, 21):
            nonce = nonce_factory.get_nonce(chars=n)
            self.assertEqual(len(nonce), n)


class ShortcutTests(TestCase):

    def test_get_shorturl(self):
        """
        Tests that we can register a URL and get its short url.
        """
        # Ensure that calling get_shortcut() with no parameters returns None
        self.assertEqual(get_shorturl(''), None)

        # Ensure SHORTURLS_CODE_LENGTH setting works
        with self.settings(SHORTURLS_CODE_LENGTH=16):
            source_url_one = 'http://www.one.com/'
            short_url_one = get_shorturl(url=source_url_one)
            # http://example.com/u/XXXXXXXXXXXXXXXX/
            self.assertEqual(len(short_url_one), 22 + 16)

        # Ensure SHORTURLS_PROTOCOL setting works
        with self.settings(SHORTURLS_PROTOCOL='https'):
            source_url_two = 'http://www.two.com/'
            short_url_two = get_shorturl(url=source_url_two)
            # https://example.com/u/XXXXXX/
            self.assertEqual(len(short_url_two), 22 + 7)
            self.assertTrue(short_url_two.startswith('https://'))

        # Ensure its producing different results for different source urls
        self.assertNotEquals(short_url_one, short_url_two)

        # Ensure shortening same source url results in the same short url
        new_short_url = get_shorturl(url=source_url_one)
        self.assertEqual(new_short_url, short_url_one)

        # Ensure that using a request object works too
        request_factory = RequestFactory()
        request = request_factory.get('/')
        self.assertEqual(
            get_shorturl(source_url_one, request=request), short_url_one)
