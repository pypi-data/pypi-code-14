"""
  Copyright (c) 2015, Tyler Finethy

  All rights reserved. See LICENSE file for details
"""
# Setup config from http://docs.cython.org
from distutils.extension import Extension
from distutils.core import setup
# Import Cython
from Cython.Build import cythonize
# Import numpy
import numpy as np

# extensions to compile
extensions=[
    Extension("GeosPy/utilities/*.pyx",
        ["GeosPy/utilities/*.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-w"]),
    Extension("GeosPy/models/*.pyx",
        ["GeosPy/models/*.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-w"]),
    Extension("GeosPy/*.pyx",
        ["GeosPy/*.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-w"])
    ]

# full config
config = {
    'description': 'GeosPy',
    'author': 'Tyler Finethy',
    'author_email': 'tylfin@gmail.com',
    'license': 'MIT',
    'url': 'https://github.com/tylfin/GeosPy',
    'download_url': 'https://github.com/tylfin/GeosPy',
    'version': '0.1.4',
    'packages': ['GeosPy', 'GeosPy.utilities', 'GeosPy.models'],
    'scripts': [],
    'install_requires': ['Cython==0.24.1', 'numpy==1.11.2', 'scipy==0.18.1'],
    'name': 'GeosPy',
    'keywords': ['Geolocation', 'Machine Learning', 'Geolocation inference'],
    'ext_modules':cythonize(extensions),
    'classifiers': ['License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5']
}

# setting up
setup(**config)
