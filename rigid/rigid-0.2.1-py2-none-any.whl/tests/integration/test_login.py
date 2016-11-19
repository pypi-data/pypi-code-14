import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class LoginTests(unittest.TestCase):
    def setUp(self):
        super(LoginTests, self).setUp()
        self.server = FakeServer()

    def test_login_success(self):
        self.server.status = 200
        self.server.body = { 'token': 'abc' }

        runner = CliRunner()
        result = runner.invoke(cli, ['login'], input='kyle@example.com\nsecretpw\n', env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/authorizations')
        self.assertEqual(self.server.request['headers']['Authorization'], 'Basic a3lsZUBleGFtcGxlLmNvbTpzZWNyZXRwdw==')

    def test_login_failure(self):
        self.server.status = 401
        self.server.body = {}

        runner = CliRunner()
        result = runner.invoke(cli, ['login'], input='kyle@example.com\nsecret\n', env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, 'Enter your Rigid credentials.\nEmail: kyle@example.com\nPassword: \nError: Invalid Credentials\n')

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/authorizations')
        self.assertEqual(self.server.request['headers']['Authorization'], 'Basic a3lsZUBleGFtcGxlLmNvbTpzZWNyZXQ=')
