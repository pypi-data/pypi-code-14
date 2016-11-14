# -*- coding: utf-8 -*-

from math import ceil, log
from Crypto.Random import random


class NonceFactory(object):

    BASE_ALPH = tuple("23456789BCDFGHJKMNPQRSTVWXYZbcdfghjkmnpqrstvwxyz")

    def __init__(self, alphabet=BASE_ALPH):
        """
        A Nonce Generator. Provide the optional param {alphabet} as a string
        of unique symbols to override the default, which is 48 alpha-numerics:
        [23456789BCDFGHJKMNPQRSTVWXYZbcdfghjkmnpqrstvwxyz]. This has some
        confusing symbols and vowels removed to reduce the chance of foul
        language words appearing in the resulting code and to aide verbal or
        written transport.
        """
        self.alphabet = alphabet
        self.base_dict = dict((c, v) for v, c in enumerate(alphabet))
        self.base_len = len(alphabet)

        #
        # This is how much larger the random bits must be to produce a number
        # of at least `digits` length of the alphabet.
        #
        self.multiplier = int(ceil(log(self.base_len, 2)))
        self.bits_per_char = log(self.base_len, 2)

    def base_decode(self, string):
        """
        Convert string of characters from generator's alphabet to raw number.
        """
        # This method is here for completeness. Won't be used much.
        num = 0
        for char in string:
            num = num * self.base_len + self.base_dict[char]
        return num

    def base_encode(self, num):
        """
        Convert number to string of characters from the generator's alphabet.
        """
        # http://stackoverflow.com/posts/14259141/revisions
        if not num:
            return self.alphabet[0]

        encoding = ""
        while num:
            num, rem = divmod(num, self.base_len)
            encoding = self.alphabet[rem] + encoding
        return encoding

    def get_alphabet(self):
        """
        Return the alphabet currently in use.
        """
        return self.alphabet

    def get_nonce(self, chars):
        """
        Returns a random code of {chars} character's long as a string of
        characters in the generator's alphabet.
        """

        #
        # If self.base_len is not an exact power of 2, then multiplier will
        # have been rounded up to the nearest integer, so, the resulting
        # base_encode may be larger than the desired number of chars. We
        # return the least significant portion, which will have more entropy
        # than the only partially fillable most-significant-digit.
        #
        # NOTE: assuming the default 48-character alphabet of BASE_ALPH:
        #      6 chars >=  33 bits entropy
        #      8 chars >=  44 bits
        #     12 chars >=  67 bits
        #     16 chars >=  89 bits
        #     20 chars >= 111 bits
        #     23 chars >= 128 bits
        #     24 chars >= 134 bits
        #
        return self.base_encode(
            random.getrandbits(chars * self.multiplier)
        ).zfill(chars)[-chars:]

    def get_nonce_of_bits(self, bits):
        """
        Returns of random code representing at least {bits} bits of entropy
        as a string of characters in the generator's alphabet.
        """
        return self.base_encode(
            random.getrandbits(
                int(ceil(bits / self.bits_per_char) * self.bits_per_char)
            )
        )

#
# Convenient instance using default, 48-symbol length alphabet
#
nonce_factory = NonceFactory()
