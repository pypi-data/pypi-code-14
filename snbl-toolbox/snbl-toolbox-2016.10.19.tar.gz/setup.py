#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from glob import glob
import subprocess
from setuptools import setup

dirname = 'SNBLToolBox'
file_frozen = '{}/frozen.py'.format(dirname)
we_run_setup = False
if not os.path.exists(file_frozen):
    we_run_setup = True
    hash_ = subprocess.Popen(['hg', 'id', '-i'], stdout=subprocess.PIPE).stdout.read().decode().strip()
    print('SNBL Toolbox mercurial hash is {}'.format(hash_))
    frozen = open(file_frozen, 'w')
    frozen.write('hg_hash = "{}"'.format(hash_))
    frozen.close()

modules = glob('{}/ui/*.py'.format(dirname))
try:
    modules.remove('{}/ui/compile.py'.format(dirname))
except ValueError:
    pass
modules += glob('{}/*.py'.format(dirname))
modules += glob('{}/roerik/*.py'.format(dirname))
modules = [s.replace('/', '.').split('.py')[0] for s in modules]

print(modules)
setup(
    name='snbl-toolbox',
    version='2016.10.19',
    description='SNBL Toolbox',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/snbltb',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
        'cryio>=2016.09.01',
        'pyqtgraph-for-dubble-bubble>=2016.10.12',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'snbl={}.__init__:main'.format(dirname),
        ],
    },
    py_modules=modules,
)

if we_run_setup:
    os.remove(file_frozen)
