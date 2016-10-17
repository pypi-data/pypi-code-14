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
    name='scalehub',

    version='1.0.0b1',

    description='Test automation framework',

    long_description=long_description,

    url='https://github.com/scalehub/scalehub',

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

    packages=['scalehub'],

    install_requires=[],

    extras_require={
        'test': ['mock>=2.0', 'pytest>=3.0'],
    },
)
