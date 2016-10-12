#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from glob import glob
import subprocess
from setuptools import setup

we_run_setup = False
if not os.path.exists('frozen.py'):
    we_run_setup = True
    hash_ = subprocess.Popen(['hg', 'id', '-i'], stdout=subprocess.PIPE).stdout.read().decode().strip()
    print('Bubble mercurial hash is {}'.format(hash_))
    frozen = open('frozen.py', 'w')
    frozen.write('hg_hash = "{}"'.format(hash_))
    frozen.close()
    frozen = open('bcommon/__init__.py', 'w')
    frozen.write('#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\nfrozen = True')
    frozen.close()

modules = glob('bclient/ui/*.py')
try:
    modules.remove('bclient/ui/compile.py')
except ValueError:
    pass
modules += glob('bclient/*.py')
modules += glob('bcommon/corrections/*.py')
modules += glob('bcommon/*.py')
modules += glob('bserver/*.py')
modules += ['frozen.py', '__init__.py']
modules = ['bubble.{}'.format(s.replace('/', '.').split('.py')[0]) for s in modules]


setup(
    name='bubble-dubble',
    version='2016.10.12.3',
    description='Azimuthal powder integration',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/bubble',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
        'simplejson>=3',
        'cryio>=2016.09.01',
        'integracio>=2016.09.01',
        'decor>=2016.09.01',
        'pyqtgraph-for-dubble-bubble>=2016.10.12',
    ],
    include_package_data=True,
    package_dir={'bubble': ''},
    entry_points={
        'console_scripts': [
            'bubbles=bubble.bserver.server:main',
            'bubblec=bubble.bclient.wbubblec:main',
        ],
    },
    py_modules=modules,
)

if we_run_setup:
    os.remove('frozen.py')
    frozen = open('bcommon/__init__.py', 'w')
    frozen.write('#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n')
    frozen.close()
