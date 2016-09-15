"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
##from os import path
import os
here = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(here, "Data")
# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='TFBS_footprinting',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0b4',

    description='Tool for identifying conserved TFBSs',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/thirtysix/TFBS_footprinting',

    # Author details
    author='Harlan Barker',
    author_email='harlan.barker@uta.fi',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],

    # What does your project relate to?
    keywords='bioinformatics analysis',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
##    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['httplib2', 'numpy', 'matplotlib', 'biopython'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
##    extras_require={
##        'dev': ['check-manifest'],
##        'test': ['coverage'],
##    },
    extras_require={},


    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
##    package_data={
##        'Data': ['pwms.json'],
##    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
##    data_files=[('my_data', ['Data/pwms.json'])],
##    data_files = [("", [os.path.join(root, f) for f in files]) for root, dirs, files in os.walk(data_dir)],
    data_files = [("", [f for f in files]) for root, dirs, files in os.walk(data_dir)],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={},
##    entry_points={
##        'console_scripts': [
##            'sample=sample:main',
##        ],
##    },

)
