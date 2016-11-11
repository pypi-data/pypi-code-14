# -*- coding: utf-8 -*-

""" basic test cases """

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from pygenerator.project import Config, Project


PYTHON3 = sys.version_info > (3, )


def is_exe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def get_version(fpath):
    with open(fpath, 'r') as f:
        content = ''.join(f.readlines())
    env = {}
    if PYTHON3:
        exec(content, env, env)
    else:
        compiled = compile(content, 'get_version', 'single')
        eval(compiled, env, env)
    return env['__version__']


class BasicTestCase(unittest.TestCase):
    """ basic cases """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self._path = tempfile.mkdtemp()
        self._cwd = os.getcwd()

    def tearDown(self):
        try:
            shutil.rmtree(self._path)
        except:
            pass
        os.chdir(self._cwd)

    def test_basic(self):
        config = Config(
            project_name='test_project',
            project_description='a basic test',
            keywords='development tools',
            url='http://itevenworks.net',
            author='joebiden',
            author_email='joe@biden.io',
            license='apache',
            scripts=['tool'],
            requires=[],
            tests_requires=['nose'],
            extras_requires=[],
            packages=['package'],
            version='1.2.3'
        )
        temppath = self._path
        project = Project(config, base_path=temppath)
        project.create()

        exists = os.path.exists
        join = os.path.join
        project_path = join(temppath, 'test_project')

        # did the script get added?
        path = join(project_path, 'bin', 'tool')
        self.assertTrue(is_exe(path))

        # check the TLD files
        self.assertTrue(
            exists(join(project_path, 'CHANGES'))
        )
        self.assertTrue(
            exists(join(project_path, 'CONTRIBUTING'))
        )
        self.assertTrue(
            exists(join(project_path, 'MANIFEST.in'))
        )
        self.assertTrue(
            exists(join(project_path, 'README.rst'))
        )
        self.assertTrue(
            exists(join(project_path, 'requirements.txt'))
        )
        self.assertTrue(
            exists(join(project_path, 'setup.py'))
        )

        # inspect the package
        path = join(project_path, 'package')
        self.assertTrue(exists(path))

        # is the version correct?
        path = join(project_path, 'package', '__init__.py')
        self.assertEquals(get_version(path), '1.2.3')

        # do tests run?
        os.chdir(project_path)
        proc = subprocess.Popen(
            args=[
                'python',
                'setup.py',
                'nosetests',
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.wait()
        self.assertEquals(proc.returncode, 0)
        self.assertIn('Ran 1 test', proc.stderr.read())
