from pip.req import parse_requirements
from setuptools import setup, find_packages
import os

DIR = os.path.dirname(os.path.abspath(__file__))

with open('README.rst') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='proso-events-client',
    version='0.0.6',
    description='Client for "event storage"."',
    long_description=README,
    author='Jan Karásek',
    author_email='xkarase1@fi.muni.cz',
    url='',
    license=LICENSE,
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['bin/proso-events-log-upload'],
    namespace_packages=['proso', 'proso.events'],
    install_requires=[
        str(r.req)
        for r in parse_requirements(DIR + '/requirements.txt', session=False)
        ]
)
