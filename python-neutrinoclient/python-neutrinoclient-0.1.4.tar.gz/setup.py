from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

install_reqs = parse_requirements('requirements.txt', session=PipSession())

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="python-neutrinoclient",
    version="0.1.4",
    description="Neutrino API Client Library",
    author="Adrian Moreno",
    author_email="adrian.moreno@emc.com",
    packages=['neutrinoclient'],
    include_package_data=True,
    keywords=['neutrino', 'openstack'],
    install_requires=reqs
)
