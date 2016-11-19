
import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer


class AppsTests(unittest.TestCase):
    def setUp(self):
        super(AppsTests, self).setUp()
        self.server = FakeServer()

    def test_app_success(self):
        self.server.status = 200
        self.server.body = {
            'name': 'test',
            'web_url': 'http://test.rigidapp.com',
        }

        runner = CliRunner()
        result = runner.invoke(cli, ['app', 'test'], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test - http://test.rigidapp.com\n')

        self.assertEqual(self.server.request['method'], 'GET')
        self.assertEqual(self.server.request['path'], '/apps/test')

    def test_app_create(self):
        self.server.status = 201
        self.server.body = {
            'name': 'test',
            'web_url': 'http://test.rigidapp.com',
        }

        runner = CliRunner()
        result = runner.invoke(cli, ['app', 'test', '--create'], input='y\n', env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test (http://test.rigidapp.com) has been created.\n')

        self.assertEqual(self.server.request['method'], 'POST')
        self.assertEqual(self.server.request['path'], '/apps')

    def test_app_delete_confirm(self):
        self.server.status = 204

        runner = CliRunner()
        result = runner.invoke(cli, ['app', 'test', '--delete'], input='y\n', env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Are you sure you want to delete test? [y/N]: y\ntest has been deleted.\n')

        self.assertEqual(self.server.request['method'], 'DELETE')
        self.assertEqual(self.server.request['path'], '/apps/test')

    def test_app_delete_no(self):
        self.server.status = 204

        runner = CliRunner()
        result = runner.invoke(cli, ['app', 'test', '--delete'], input='n\n', env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 1)

        self.assertEqual(len(self.server.requests), 0)

    def test_app_rename(self):
        self.server.status = 200
        self.server.body = {'name': 'new'}

        runner = CliRunner()
        result = runner.invoke(cli, ['app', 'test', '--rename', 'new'], env={'RIGID_API': self.server.url}, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test has been renamed to new.\n')

        self.assertEqual(self.server.request['method'], 'PATCH')
        self.assertEqual(self.server.request['path'], '/apps/test')
