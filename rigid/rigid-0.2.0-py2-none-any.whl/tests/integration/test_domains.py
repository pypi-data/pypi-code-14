import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class DomainTests(unittest.TestCase):
    def setUp(self):
        super(DomainTests, self).setUp()
        self.server = FakeServer()

    def test_add_domain(self):
        self.server.status = 202
        self.server.body = {}

        runner = CliRunner()
        result = runner.invoke(cli, ['domains', '--add', 'example.com', '-a', 'test'], env={'RIGID_API': self.server.url}, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'example.com has been added to test.\n')

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/apps/test/aliases/production/domains')

    def test_remove_domain(self):
        self.server.status = 204

        runner = CliRunner()
        result = runner.invoke(cli, ['domains', '--remove', 'example.com', '-a', 'test'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'example.com has been removed from test.\n')

        self.assertEqual(self.server.request['method'], 'DELETE')
        self.assertEqual(self.server.request['path'], '/apps/test/aliases/production/domains/example.com')
