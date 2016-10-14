# -*- coding: utf-8 -*-
import unittest
from tag_processor import DataContainer, TagParser


class TagParserTest(unittest.TestCase):

    def test_single_attribute(self):
        data = DataContainer()
        parser = TagParser(data)
        input_string = u"[get_cost]"
        elements = parser._split_by_elements(input_string)
        self.assertEqual(elements[0], '[get_cost]')

    def test_attribute_parameter_with_double_underscores(self):
        data = DataContainer()
        data.warehouse = dict()
        data.warehouse['storage'] = dict()
        data.warehouse['storage']['cargo'] = [{
            'name': 'mirror',
            'quantity': 12
        }, {
            'name': 'wheel',
            'quantity': 45
        }]

        input = "[random__warehouse]__warehouse[get_name]__storage[max=cargo__quantity]__name_"
        parser = TagParser(data)
        elements = parser._split_by_elements(input)
        self.assertEqual(len(elements), 4)
        self.assertEqual(elements[0], "[random__warehouse]")
        self.assertEqual(elements[1], "warehouse[get_name]")
        self.assertEqual(elements[2], "storage[max=cargo__quantity]")
        self.assertEqual(elements[3], "name_")


    def test_inline_tags(self):
        input_string = "${${warning_message}|${error_message}}"
        parser = TagParser(None)
        tags = parser._get_tags(input_string)

        self.assertEqual(tags[1], [ 'warning_message', 'error_message' ])
        self.assertEqual(tags[0], [
            '${warning_message}|${error_message}'
        ])

