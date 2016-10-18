import os
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '-s',
            '-ra',
            '--verbose',
            '--flake8',
            '--isort',
            '--cov-report=xml',
            '--cov-report=term-missing',
            '--cov=scrumotron',
            '--junitxml=junit.xml',
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'scrumotron', 'version.txt')) as f:
    VERSION = f.read().strip()

setup(
    name="scrum-o-tron",
    version=VERSION,
    license="MIT",
    description="Slack BOT that implements a very simple standup.",
    long_description=README,
    url="",
    keywords="python slack bot",
    packages=find_packages(),
    cmdclass={'test': PyTest},
    tests_require=[
        'flake8==3.0.4',
        'pytest==3.0.3',
        'pytest-flake8==0.8.1',
        'pytest-isort==0.1.0',
        'flake8-isort==2.0.1',
        'pytest-cov',
        'setuptools',
        'slackclient',
    ],
    install_requires=[
        'setuptools',
        'slackclient',
    ],
    dependency_links=[
    ],
    package_data={
        '': ['*.txt', '*.rst', '*.md', '*.json', '*.conf'],
    },
    entry_points={
        'console_scripts': [
            'scrumotron = scrumotron.cli:main'
        ]
    },
    classifiers=[
        # Development Status: 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
