#!/usr/bin/env python2
from setuptools import setup

if __name__ == '__main__':
    setup(
        name='easydir',
        description='Easy parent directory selection',
        author='Viet Nguyen',
        author_email='vietjtnguyen@gmail.com',
        url='https://github.com/vietjtnguyen/easydir/',
        version='0.1.0',
        scripts=['easydir'],
        classifiers=[
            'Environment :: Console',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2',
            'Topic :: System',
        ],
    )
