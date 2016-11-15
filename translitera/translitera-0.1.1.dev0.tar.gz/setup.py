# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 19:24:50 2016

@title: setup.py
@author: Srikanth Anantharam <srikanth_anantharam@linux.com>
@purpose: setup script for the translitera package
"""

import setuptools
from codecs import open

if __name__ == '__main__':
    setuptools.setup(
        name='translitera',
        version='0.1.1.dev0',

        description='Phonetic transliteration of text in Kannaḍa script into Latin/English characters',
        long_description=open('translitera/README.reSTful').read(),

        url='https://github.com/sria91/translitera',
        download_url='https://github.com/sria91/translitera',

        author='Srikanth Anantharam',
        author_email='saprao@linux.com',

        packages=setuptools.find_packages(),

        license='Apache Software License',

        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.5',
        ],

        keywords=['translitera'],

        package_data={ 'translitera' : [
            'README.reSTful', 
            'LICENSE.txt', 
#            'kannaḍa_to_english.json',
#            'kannaḍa_to_english_2.json',
            'kannaḍa_to_latin.json'],
        },

        entry_points={
            'console_scripts': [
            'translitera = translitera:main',
            ],
        },
    )
