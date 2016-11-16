from flask import json
from flask_restful import reqparse
import mox

from shinkansen.http import common


class TestCommon(mox.MoxTestBase):
    def parser_setup(self, args):
        orig_RequestParser = reqparse.RequestParser
        self.mox.StubOutWithMock(reqparse, 'RequestParser')
        parser = self.mox.CreateMock(orig_RequestParser)
        reqparse.RequestParser().AndReturn(parser)
        parser.add_argument('key', type=str, help=mox.IgnoreArg())
        parser.parse_args().AndReturn(args)

    def test_keyed_returns_original_result(self):
        self.parser_setup({})
        self.mox.ReplayAll()
        data = {'abc': 123, 'def': 456}
        self.assertEqual(common.keyed(lambda: data)(), data)

    def test_keyed_ignores_None(self):
        self.parser_setup({'key': None})
        self.mox.ReplayAll()
        data = {'abc': 123, 'def': 456}
        self.assertEqual(common.keyed(lambda: data)(), data)

    def test_keyed_returns_only_key_value(self):
        key = 'abc'
        self.parser_setup({'key': key})
        self.mox.ReplayAll()
        data = {'abc': 123, 'def': 456}
        self.assertEqual(common.keyed(lambda: data)(), data[key])

    def test_keyed_fails_if_key_not_in_data(self):
        key = 'cba'
        self.parser_setup({'key': key})
        response = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(json, 'jsonify')
        json.jsonify({'error': mox.IgnoreArg()}).AndReturn(response)
        response.status_code = 400
        self.mox.ReplayAll()
        data = {'abc': 123, 'def': 456}
        self.assertEqual(common.keyed(lambda: data)(), response)
