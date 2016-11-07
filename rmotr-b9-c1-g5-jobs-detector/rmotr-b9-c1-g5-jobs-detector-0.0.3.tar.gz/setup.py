import os
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["tests/"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import sys, pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='rmotr-b9-c1-g5-jobs-detector',
    version='0.0.3',
    description="rmotr.com Group Project | Jobs Detector",
    author='Delio Castillo',
    author_email='jangeador@gmail.com',
    url='https://github.com/jangeador/pyp-w3-gw-jobs-detector',
    license='CC BY-SA 4.0 License',
    packages=['jobs_detector'],
    maintainer='rmotr.com',
    install_requires=[
        'bs4',
        'click',
        'requests_cache'
    ],
    entry_points={
        'console_scripts':['jobs_detector=jobs_detector.main:jobs_detector']
    },
    tests_require=[
        'pytest==2.9.1'
    ],
    zip_safe=False,
    cmdclass={'test': PyTest},
)
