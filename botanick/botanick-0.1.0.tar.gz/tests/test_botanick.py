#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_botanick
----------------------------------

Tests for `botanick` module.
"""
import unittest
from botanick import Botanick


class TestBotanickMethods(unittest.TestCase):

	@classmethod
	def test_botanick(cls):
		emails_found = Botanick.search("squad.pro")
		assert emails_found != ""

if __name__ == '__main__':
    unittest.main()