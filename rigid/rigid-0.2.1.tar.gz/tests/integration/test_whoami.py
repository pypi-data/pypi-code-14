import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class WhoamiTests(unittest.TestCase):
    def setUp(self):
        super(WhoamiTests, self).setUp()
        self.server = FakeServer()

    def test_whoami_success(self):
        self.server.status = 200
        self.server.body = { 'email': 'kyle@example.com' }

        runner = CliRunner()
        result = runner.invoke(cli, ['whoami'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'kyle@example.com\n')

        self.assertEqual(self.server.request['method'], 'GET')
        self.assertEqual(self.server.request['path'], '/user')
