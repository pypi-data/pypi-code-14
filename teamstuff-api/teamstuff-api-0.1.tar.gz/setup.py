from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup


setup(
    name='teamstuff-api',
    version='0.1',
    author='Tom Werner',
    author_email='hello@tomwerner.me.uk',
    packages=['teamstuff-api'],
    url='https://gitlab.com/tomwerneruk/teamstuff-api',
    license='See LICENSE.txt',
    description='',
    long_description=open('README.txt').read(),
)
