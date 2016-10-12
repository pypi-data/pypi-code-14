#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

setup(
    name='cryio',
    version='2016.10.12',
    description='Crystallographic IO routines',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/cryio',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
        'jinja2>=2.7',
        'six>=1.9'
    ],
    package_dir={'cryio': ''},
    py_modules=[
        'cryio.__init__',
        'cryio.cbfimage',
        'cryio.ccp4image',
        'cryio.crysalis',
        'cryio.edfimage',
        'cryio.esperanto',
        'cryio.fit2dmask',
        'cryio.mar345image',
        'cryio.numpymask',
        'cryio.parparser',
        'cryio.tools',
        'cryio.templates.__init__',
        'cryio.templates.tplcbf',
        'cryio.templates.tplcrys',
        'cryio.templates.tpledf',
        'cryio.templates.tplesp',
    ],
    ext_modules=[
        Extension(
            'cryio._cryio', [
                'src/cryiomodule.c',
                'src/agi_bitfield.c',
                'src/byteoffset.c',
                'src/ccp4.c',
                'src/mar345.c',
            ],
            extra_compile_args=['-O2'],
        )
    ],
)
