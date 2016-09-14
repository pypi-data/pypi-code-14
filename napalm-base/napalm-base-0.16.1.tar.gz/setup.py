"""setup.py file."""
import uuid

from setuptools import setup, find_packages
from pip.req import parse_requirements
from napalm_base import system_helpers

__author__ = 'David Barroso <dbarrosop@dravetech.com>'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="napalm-base",
    version=system_helpers.find_version('napalm_base', '__init__.py'),
    packages=find_packages(),
    author="David Barroso",
    author_email="dbarrosop@dravetech.com",
    description="Network Automation and Programmability Abstraction Layer with Multivendor support",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/napalm-automation/napalm-base",
    include_package_data=True,
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            'cl_napalm_configure=napalm_base.clitools.cl_napalm_configure:main',
            'cl_napalm_test=napalm_base.clitools.cl_napalm_test:main'
        ],
    }
)
