#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='giusas',
    version='2016.11.4',
    description='GISAXS and GIWAXS calculator',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/giusas',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
        'scipy>=0.10.0',
        'pyqtgraph-for-dubble-bubble>=2016.10.12',
        'cryio>=2016.10.1',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'giusas=giusas.__init__:main',
        ],
    },
    py_modules=[
        'giusas.gui.ui.__init__',
        'giusas.gui.ui.wgiusas',
        'giusas.gui.ui.resources_rc',
        'giusas.gui.ui.wtab',
        'giusas.gui.__init__',
        'giusas.gui.imageview',
        'giusas.gui.ptree',
        'giusas.gui.tabs',
        'giusas.gui.wgiusas',
        'giusas.__init__',
        'giusas.controller',
        'giusas.model',
    ],
)
