from os import path
import sys
from codecs import open
from setuptools import setup, find_packages

exec(open('iperf_graphite/version.py').read())

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r', 'utf-8') as f:
    readme = f.read()

with open(path.join(here, 'LICENSE'), 'r', 'utf-8') as f:
    license = f.read()

requirements=['iperf3', 'PyYAML']

setup(
    name = "iperf_graphite",
    version = __version__,
    author = "Carlos Vicente",
    author_email = "cvicente@dyn.com",
    description = ("Run iperf tests in both directions and send results to Graphite"),
    license = license,
    keywords = "iperf3 graphite",
    url = "https://github.com/dyninc/iperf_graphite",
    long_description=readme,
    classifiers=[
        "Topic :: Utilities",
        'Programming Language :: Python',
        'Topic :: System :: Networking'
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=requirements,
    test_suite='nose.collector',
    tests_require=['nose'] + requirements,
    entry_points = {
        'console_scripts': ['iperf_graphite=iperf_graphite.iperf_graphite:main'],
    },
    include_package_data=True
)
