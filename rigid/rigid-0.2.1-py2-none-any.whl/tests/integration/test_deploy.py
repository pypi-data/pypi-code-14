import os
import unittest
from click.testing import CliRunner

from rigid.commands import cli

from ..utils import FakeServer

FIXTURES = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

class DeployTests(unittest.TestCase):
    def setUp(self):
        super(DeployTests, self).setUp()
        self.server = FakeServer()

        self.server.status = 200
        self.server.responses = [
            # Preflight (head)
            {},

            # Create Source
            {'body': {'uuid': 'source-uuid', 'upload': {'method': 'PUT', 'url': self.server.url + '/upload-source'}}},

            # Upload Source
            {},

            # Create version
            {'body': {'uuid': 'version-uuid'}},

            # Promote version
            {'body': {}},
        ]

    def test_deploy_without_app(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['deploy', FIXTURES], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.output, 'Usage: cli deploy [OPTIONS] SOURCE\n\nError: Missing option "--app" / "-a".\n')


    def test_deploy_success(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['deploy', '-a', 'testingapp', FIXTURES], env={'RIGID_API': self.server.url}, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(self.server.requests),  5)

        # Preflight (to check auth and permissions to app)
        self.assertEqual(self.server.requests[0]['method'],  'HEAD')
        self.assertEqual(self.server.requests[0]['path'],  '/apps/testingapp')

        # Create a source
        self.assertEqual(self.server.requests[1]['method'],  'POST')
        self.assertEqual(self.server.requests[1]['path'],  '/sources')

        # Upload source
        self.assertEqual(self.server.requests[2]['method'],  'PUT')
        self.assertEqual(self.server.requests[2]['path'],  '/upload-source')

        # Create version
        self.assertEqual(self.server.requests[3]['method'],  'POST')
        self.assertEqual(self.server.requests[3]['path'],  '/apps/testingapp/versions')

        # Promote version
        self.assertEqual(self.server.requests[4]['method'],  'PUT')
        self.assertEqual(self.server.requests[4]['path'],  '/apps/testingapp/aliases/production')

    def test_deploy_create(self):
        self.server.responses = [
            {'body': {'name': 'testingapp'}}
        ] + self.server.responses[1:]

        runner = CliRunner()
        result = runner.invoke(cli, ['deploy', '--create', '-a', 'testingapp', FIXTURES], env={'RIGID_API': self.server.url}, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(self.server.requests),  5)

        # Preflight (to check auth and permissions to app)
        self.assertEqual(self.server.requests[0]['method'],  'POST')
        self.assertEqual(self.server.requests[0]['path'],  '/apps')

        # Create a source
        self.assertEqual(self.server.requests[1]['method'],  'POST')
        self.assertEqual(self.server.requests[1]['path'],  '/sources')

        # Upload source
        self.assertEqual(self.server.requests[2]['method'],  'PUT')
        self.assertEqual(self.server.requests[2]['path'],  '/upload-source')

        # Create version
        self.assertEqual(self.server.requests[3]['method'],  'POST')
        self.assertEqual(self.server.requests[3]['path'],  '/apps/testingapp/versions')

        # Promote version
        self.assertEqual(self.server.requests[4]['method'],  'PUT')
        self.assertEqual(self.server.requests[4]['path'],  '/apps/testingapp/aliases/production')

    def test_deploy_create_random_name(self):
        self.server.responses = [
            {'body': {'name': 'rando'}}
        ] + self.server.responses[1:]

        runner = CliRunner()
        result = runner.invoke(cli, ['deploy', '--create', FIXTURES], env={'RIGID_API': self.server.url})
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(self.server.requests),  5)

        # Preflight (to check auth and permissions to app)
        self.assertEqual(self.server.requests[0]['method'],  'POST')
        self.assertEqual(self.server.requests[0]['path'],  '/apps')

        # Create a source
        self.assertEqual(self.server.requests[1]['method'],  'POST')
        self.assertEqual(self.server.requests[1]['path'],  '/sources')

        # Upload source
        self.assertEqual(self.server.requests[2]['method'],  'PUT')
        self.assertEqual(self.server.requests[2]['path'],  '/upload-source')

        # Create version
        self.assertEqual(self.server.requests[3]['method'],  'POST')
        self.assertEqual(self.server.requests[3]['path'],  '/apps/rando/versions')

        # Promote version
        self.assertEqual(self.server.requests[4]['method'],  'PUT')
        self.assertEqual(self.server.requests[4]['path'],  '/apps/rando/aliases/production')
