from setuptools import setup
from os import path
from unix_dates import __version__

here = path.abspath(path.dirname(__file__))

setup(
    name='itculate_sdk',
    version=__version__,
    description='ITculate SDK',
    url='https://bitbucket.org/itculate/itculate-sdk',
    author='Ophir',
    author_email='opensource@itculate.io',
    license='MIT',
    keywords=['ITcualte', 'sdk', 'graph', 'topology'],
    packages=['itculate_sdk'],
)
