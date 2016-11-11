import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class TokenTests(unittest.TestCase):
    def setUp(self):
        super(TokenTests, self).setUp()
        self.server = FakeServer()

    def test_token_success(self):
        self.server.status = 200
        self.server.body = { 'token': 'abc' }

        runner = CliRunner()
        result = runner.invoke(cli, ['token'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'abc\n')

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/authorizations')
