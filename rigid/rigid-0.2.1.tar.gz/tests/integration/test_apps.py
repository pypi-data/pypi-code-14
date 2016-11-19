import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class AppsTests(unittest.TestCase):
    def setUp(self):
        super(AppsTests, self).setUp()
        self.server = FakeServer()

    def test_apps_success(self):
        self.server.status = 200
        self.server.body = [
            {'name': 'test'},
            {'name': 'palaver'},
        ]

        runner = CliRunner()
        result = runner.invoke(cli, ['apps'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test\npalaver\n')

        self.assertEqual(self.server.request['method'], 'GET')
        self.assertEqual(self.server.request['path'], '/apps')
