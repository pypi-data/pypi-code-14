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
    name='pyrnkr',
    description='RNKR interface for Python',
    long_description=long_description,
    keywords='pyrnkr, rnkr, python',
    packages=find_packages(exclude=['docs', 'examples']),
    install_requires=requirements,
    version='8.0',
    author='Isaac Elbaz',
    author_email='isaac@rnkr.io',
    url='https://rnkr.io'
)
