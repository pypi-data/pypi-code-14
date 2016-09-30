"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scalerunner',

    version='1.0.0a2',

    description='PyScale plugin for remote programs running',

    long_description=long_description,

    url='https://github.com/pyscale/scalerunner',

    author='PyScale team',

    author_email='wedonthaveemailyet@pyscale.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='testing automation',

    packages=['scalerunner'],

    install_requires=[
        'spur>=0.3',
    ],
)
