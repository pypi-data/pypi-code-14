from os import path

from pip.req import parse_requirements
from setuptools import setup, find_packages

# mark our location
here = path.abspath(path.dirname(__file__))

# obtain the long description
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

raw_requirements = parse_requirements(
    path.join(here, 'requirements.txt'), session=False)

requirements = [str(x.req) for x in raw_requirements]

setup(
    name='rnkrcli',
    description='RNKR Client Interface',
    long_description=long_description,
    keywords='rnkr, rnkr client, rnkrcli',
    include_package_data=True,
    packages=find_packages(exclude=['docs']),
    package_data={
        'rnkrcli': [
            'templates/*'
        ]
    },
    install_requires=requirements,
    scripts=['rnkrcli/bin/rnkr'],
    version='9.0',
    author='Isaac Elbaz',
    author_email='isaac@rnkr.io',
    url='https://rnkr.io'
)
