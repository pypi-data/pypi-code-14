import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class TokenTests(unittest.TestCase):
    def setUp(self):
        super(TokenTests, self).setUp()
        self.server = FakeServer()

        self.server.status = 200
        self.server.body = { 'token': 'abc' }

    def test_token_success(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['token'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'abc\n')

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/authorizations')

    def test_token_with_scopes(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['token', '--scope', 'example'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'abc\n')

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/authorizations')
