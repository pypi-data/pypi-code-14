#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main, TestCase

from grako.model import ModelBuilderSemantics

from j1bz.expression.walker import Walker
from j1bz.expression.parser import get_parser


class CrudTest(TestCase):
    def setUp(self):
        self.parser = get_parser(semantics=ModelBuilderSemantics())
        self.walker = Walker()

    def test_values(self):
        created_values = [
            ("CREATE VALUES k: v;", "CREATE {k: v}"),
            ("CREATE VALUES k: v.field.field;", "CREATE {k: v.field.field}"),
            ("CREATE VALUES k: f();", "CREATE {k: f()}"),
            ("CREATE VALUES k: f(v1.f, v2.f);", "CREATE {k: f(v1.f, v2.f)}"),
            ("CREATE VALUES k: f(g());", "CREATE {k: f(g())}"),
            ("CREATE VALUES k: 'v';", "CREATE {k: u'v'}"),
            ('CREATE VALUES k: "v";', "CREATE {k: u'v'}"),
            ("CREATE VALUES k: 1;", "CREATE {k: 1}"),
            ("CREATE VALUES k: 1.1;", "CREATE {k: 1.1}"),
            ("CREATE VALUES k: TRUE;", "CREATE {k: True}"),
            ("CREATE VALUES k: FALSE;", "CREATE {k: False}"),
            ("CREATE VALUES k: NULL;", "CREATE {k: None}"),
        ]

        for value, expected in created_values:
            model = self.parser.parse(value)
            res = self.walker.walk(model)

            self.assertEqual(repr(res), expected)

    def test_create(self):
        creates = [
            ("INSERT VALUES k:v;", "CREATE {k: v}"),
            (
                "INSERT VALUES k1:v1, k2:v2;",
                ("CREATE {k1: v1, k2: v2}", "CREATE {k2: v2, k1: v1}")
            ),
            ("INSERT INTO i VALUES k:v;", "CREATE i:{k: v}"),
            ("INSERT VALUES k:v; AS i", "CREATE {k: v} AS i"),

            ("CREATE VALUES k:v;", "CREATE {k: v}"),
            (
                "CREATE VALUES k1:v1, k2:v2;",
                ("CREATE {k1: v1, k2: v2}", "CREATE {k2: v2, k1: v1}")
            ),
            ("CREATE INTO i VALUES k:v;", "CREATE i:{k: v}"),
            ("CREATE VALUES k:v; AS i", "CREATE {k: v} AS i"),
        ]

        for create, expected in creates:
            model = self.parser.parse(create)
            res = self.walker.walk(model)

            if isinstance(expected, str):
                self.assertEqual(repr(res), expected)

            elif isinstance(expected, tuple):
                at_least_one_ok = False
                for maybe in expected:
                    at_least_one_ok |= (repr(res) == maybe)

                self.assertTrue(at_least_one_ok)

    def test_read(self):
        reads = [
            ("READ r;", "READ r"),

            ("SELECT ALL;", "READ all"),
            ("SELECT s;", "READ s"),
            ("SELECT s WHERE w;", "READ s WHERE w"),
            ("SELECT s GROUP BY g;", "READ s GROUP BY g"),
            ("SELECT s ORDER BY o;", "READ s ORDER BY [(o, u'ASC')]"),
            ("SELECT s LIMIT 10;", "READ s LIMIT 10"),
            # TODO: Fix repr method to display dparams correctly
            # ("SELECT s WITH 'k':v;", "READ s"),
            ("SELECT s; AS mys", "READ s AS mys"),

            (
                "SELECT s WHERE wh GROUP BY g ORDER BY o LIMIT 10; AS mys",
                (
                    "READ s LIMIT 10 GROUP BY g ORDER BY [(o, u'ASC')] "
                    "WHERE wh AS mys"
                )
            ),

            ("SELECT a, b, c;", "READ a, b, c"),
            ("SELECT f();", "READ f()"),
            ("SELECT f(a, b, c);", "READ f(a, b, c)"),

            ("SELECT s WHERE (a);", "READ s WHERE a"),
            ("SELECT s WHERE (a = b);", "READ s WHERE =(a, b)"),
            ("SELECT s WHERE (a != b);", "READ s WHERE (a != b)"),
            ("SELECT s WHERE (a > b);", "READ s WHERE (a > b)"),
            ("SELECT s WHERE (a >= b);", "READ s WHERE (a >= b)"),
            ("SELECT s WHERE (a < b);", "READ s WHERE (a < b)"),
            ("SELECT s WHERE (a <= b);", "READ s WHERE (a <= b)"),
            ("SELECT s WHERE (a IN b);", "READ s WHERE (a in b)"),
            ("SELECT s WHERE (a NIN b);", "READ s WHERE nin(a, b)"),
            ("SELECT s WHERE (a LIKE b);", "READ s WHERE (a %% b)"),

            ("SELECT s WHERE (a AND b);", "READ s WHERE (a & b)"),
            ("SELECT s WHERE (a OR b);", "READ s WHERE (a | b)"),

            (
                "SELECT s WHERE ((a OR b) AND c);",
                "READ s WHERE ((a | b) & c)"
            ),
            (
                "SELECT s WHERE (a OR (b AND c));",
                "READ s WHERE (a | (b & c))"
            ),
            (
                "SELECT s WHERE ((a > b) AND c);",
                "READ s WHERE ((a > b) & c)"
            ),
            (
                "SELECT s WHERE (a OR (b LIKE c));",
                "READ s WHERE (a | (b %% c))"
            ),

            (
                "SELECT s ORDER BY o1, o2;",
                "READ s ORDER BY [(o1, u'ASC'), (o2, u'ASC')]"
            ),
            (
                "SELECT s ORDER BY o1 DESC, o2, o3 ASC;",
                "READ s ORDER BY [(o1, u'DESC'), (o2, u'ASC'), (o3, u'ASC')]"
            ),
        ]

        for read, expected in reads:
            model = self.parser.parse(read)
            res = self.walker.walk(model)

            self.assertEqual(repr(res), expected)

    def test_update(self):
        updates = [
            ("UPDATE VALUES k:v;", "UPDATE {k: v}"),
            ("UPDATE INTO u VALUES k:v;", "UPDATE u:{k: v}"),
            ("UPDATE VALUES k:v WHERE w;", "UPDATE {k: v} WHERE (w)"),
            ("UPDATE INTO u VALUES k:v WHERE w;", "UPDATE u:{k: v} WHERE (w)"),

            (
                "UPDATE INTO u VALUES k1:v1, k2:v2;",
                ("UPDATE u:{k1: v1, k2: v2}", "UPDATE u:{k2: v2, k1: v1}")
            ),

            ("UPDATE VALUES k:v; AS myu", "UPDATE {k: v} AS myu"),

            # TODO: WITH
        ]

        for update, expected in updates:
            model = self.parser.parse(update)
            res = self.walker.walk(model)

            if isinstance(expected, str):
                self.assertEqual(repr(res), expected)

            elif isinstance(expected, tuple):
                at_least_one_ok = False
                for maybe in expected:
                    at_least_one_ok |= (repr(res) == maybe)

                self.assertTrue(at_least_one_ok)

    def test_delete(self):
        deletes = [
            ("DELETE d;", "DELETE d"),
            ("DELETE d1, d2, d3;", "DELETE d1, d2, d3"),
            ("DELETE d WHERE w;", "DELETE d WHERE w"),
            ("DELETE d1, d2, d3 WHERE w;", "DELETE d1, d2, d3 WHERE w"),
            ("DELETE d; AS myd", "DELETE d AS myd"),
        ]

        for delete, expected in deletes:
            model = self.parser.parse(delete)
            res = self.walker.walk(model)

            self.assertEqual(repr(res), expected)


if __name__ == '__main__':
    main()
