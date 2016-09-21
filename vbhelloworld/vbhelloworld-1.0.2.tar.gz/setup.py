"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from os.path import expanduser

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vbhelloworld',
    version='1.0.2',
    description='A hello world Python project',
    long_description=long_description,
    url='https://github.com/vborrego/vbhelloworld',
    author='Vitor Borrego',
    author_email='vitor.mln.borrego@gmail.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='vbhelloworld setuptools development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pyyaml'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    #data_files=[('/etc', ['data/helloworld.conf'])],
    data_files=[( expanduser('~'), ['data/helloworld.conf'])],
    #data_files=[('etc', ['data/helloworld.conf'])],

    entry_points={
        'console_scripts': [
            'helloworld=vbhelloworld:main',
        ],
    },
)

