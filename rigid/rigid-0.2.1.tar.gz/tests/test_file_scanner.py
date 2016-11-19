import os
import tempfile
import tarfile
import unittest

from rigid.file_scanner import scan, tar, Skipper

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


class FileScannerTests(unittest.TestCase):
    def test_scan_directory(self):
        path = os.path.join(FIXTURES, 'scanner')
        files = scan(path)

        self.assertEqual(set(files), set([
            'index.html',
            'posts/hello-internet.html',
            'posts/hello-world.html',
            'posts/index.html',
        ]))


class TarTests(unittest.TestCase):
    def test_tar(self):
        fd = tempfile.NamedTemporaryFile()
        path = os.path.join(FIXTURES, 'scanner')
        tar(fd.name, ['posts/hello-internet.html', 'index.html'], path)

        with tarfile.open(fd.name) as tarball:
            self.assertEqual(tarball.getnames(), ['posts/hello-internet.html', 'index.html'])

            post = tarball.getmember('index.html')
            self.assertEqual(post.size, 13)
            self.assertEqual(post.type, tarfile.REGTYPE)

            post = tarball.getmember('posts/hello-internet.html')
            self.assertEqual(post.size, 16)
            self.assertEqual(post.type, tarfile.REGTYPE)

        fd.close()


class SkipperTests(unittest.TestCase):
    def test_skipper_default_rules(self):
        skipper = Skipper([])

        rules = [
            '.git',
            '.DS_Store',
            '.rigid.yaml',
            '.rigid-*.yaml',

            # Vim swap files
            '*~',
            '*.swp',
            '*.swo',
        ]

        self.assertEqual(skipper.rules, rules)
        self.assertEqual(skipper.DEFAULT_RULES, rules)

    def test_skipper_component(self):
        skipper = Skipper(['ignored'])

        self.assertFalse(skipper.test('hello-world.html'))
        self.assertFalse(skipper.test('ignored.html'))
        self.assertTrue(skipper.test('ignored'))
        self.assertTrue(skipper.test('ignored/index.html'))
        self.assertTrue(skipper.test('deep/ignored/index.html'))
        self.assertTrue(skipper.test('directory/ignored'))

    def test_skipper_wildcard(self):
        skipper = Skipper(['*.html'])

        self.assertFalse(skipper.test('hello-html'))
        self.assertFalse(skipper.test('html'))
        self.assertTrue(skipper.test('test.html'))
        self.assertTrue(skipper.test('testing/test.html'))

    def test_callable(self):
        skipper = Skipper(['ignored'])
        self.assertFalse(skipper('ignored'))
        self.assertTrue(skipper('not-ignored'))

    def test_skipper_from_path(self):
        path = os.path.join(FIXTURES, 'skipper')
        skipper = Skipper.open(path)
        self.assertEqual(skipper.rules, ['*.py', 'foo', 'bar'] + skipper.DEFAULT_RULES)
