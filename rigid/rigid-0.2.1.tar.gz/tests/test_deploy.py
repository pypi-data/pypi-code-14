import os
import unittest
from threading import Thread

from six.moves import BaseHTTPServer

from rigid.api import Client
from rigid.deploy import Deploy

from .utils import FakeServer

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


class DeployTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.deploy = Deploy(self.client, os.path.join(FIXTURES, 'scanner'))

    def test_collect_files(self):
        self.assertEqual(self.deploy.collect_files(), [
            'index.html',
            'posts/hello-internet.html',
            'posts/hello-world.html',
            'posts/index.html',
        ])

    def test_collect_files_with_ignore_file(self):
        deploy = Deploy(self.client, FIXTURES)
        self.assertEqual(deploy.collect_files(), [
            'scanner/index.html',
            'scanner/posts/index.html',
        ])
