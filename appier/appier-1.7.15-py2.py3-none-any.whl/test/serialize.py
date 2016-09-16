#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import unittest

import appier

class SerializeTest(unittest.TestCase):

    def test_csv(self):
        result = appier.serialize_csv([["item"], ["hello world"]])
        self.assertEqual(result, "item\r\nhello world\r\n")

        result = appier.serialize_csv([
            [appier.legacy.u("item")],
            [appier.legacy.u("hello world")]
        ])
        self.assertEqual(result, "item\r\nhello world\r\n")

        result = appier.serialize_csv([
            [appier.legacy.u("item")],
            [appier.legacy.u("你好世界")]
        ])
        self.assertEqual(result, "item\r\n你好世界\r\n")

        result = appier.serialize_csv([dict(item = "hello world")])
        self.assertEqual(result, "item\r\nhello world\r\n")

        result = appier.serialize_csv([dict(item = appier.legacy.u("hello world"))])
        self.assertEqual(result, "item\r\nhello world\r\n")

        result = appier.serialize_csv([dict(item = appier.legacy.u("你好世界"))])
        self.assertEqual(result, "item\r\n你好世界\r\n")
