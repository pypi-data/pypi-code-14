import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class PromoteTests(unittest.TestCase):
    def setUp(self):
        super(PromoteTests, self).setUp()
        self.server = FakeServer()

    def test_promote(self):
        self.server.status = 200
        self.server.body = {'version': 'testing'}

        runner = CliRunner()
        result = runner.invoke(cli, ['promote', '-a', 'test', 'abc'], env={'RIGID_API': self.server.url}, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test/production is now running testing.\n')

        self.assertEqual(self.server.request['method'], 'PUT')
        self.assertEqual(self.server.request['path'], '/apps/test/aliases/production')
