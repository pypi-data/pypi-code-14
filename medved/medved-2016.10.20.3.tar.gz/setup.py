#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='medved',
    version='2016.10.20.3',
    description='Modulation Enhanced Diffraction Viewer and EDitor',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/medved',
    license='GPLv3',
    long_description='Do not forget to cite: https://doi.org/10.1107/S2053273316008378',
    install_requires=[
        'numpy>=1.9',
        'scipy>=0.10.0',
        'fortranformat>=0.2.5',
        'pyqtgraph-for-dubble-bubble>=2016.10.12',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'medved=medved.__init__:main',
        ],
    },
    py_modules=[
        'medved.ui.__init__',
        'medved.ui.ui_wabout',
        'medved.ui.resources_rc',
        'medved.ui.ui_sliders',
        'medved.ui.ui_wmedeval',
        'medved.__init__',
        'medved.controller',
        'medved.filereader',
        'medved.imageview',
        'medved.model',
        'medved.plotwidget',
        'medved.wmedeval',
        'medved.wsliders',
    ],
)
