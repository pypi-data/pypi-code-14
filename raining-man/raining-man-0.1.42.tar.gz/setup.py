# -*- coding: utf-8 -*-
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os
import codecs
from setuptools import setup, find_packages

# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'raining_man', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'Gustavo Lopes de Brito'
''' % version
# with open(path, 'w') as F:
#     F.write(meta)

setup(
        # Basic info
        name='raining-man',
        version=version,
        author='Gustavo Lopes de Brito',
        author_email='gustavo.ldbrito@gmail.com',
        url='https://github.com/fis-jogos/ep1-rainining-man',
        description='ITS RAINING MAN!',
        long_description=codecs.open('README.rst', 'rb', 'utf8').read(),

        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            ],

        # Packages and dependencies
        package_dir={'': 'src'},
        packages=find_packages('src'),
        include_package_data=True,
        package_data={
            'raining_man.images' : ['*.png'],
            'raining_man.sounds' : ['*.mp3']
            },

        install_requires=[
            ],
        extras_require={
            'dev': [
                'python-boilerplate[dev]',
                ],
            },

        # Other configurations
        # zip_safe=False,
        platforms='any',

        entry_points={
            'console_scripts': [
                'raining_man=raining_man.run:render_game',
                ],
            },
        )
