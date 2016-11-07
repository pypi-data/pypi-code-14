# -*- coding: utf-8 -*-
from __future__ import with_statement
from setuptools import setup
from setuptools.command.test import test as TestCommand


def get_version(fname='pi_naming.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='pi-naming',
    version=get_version(),
    description="Check PI naming conventions, plugin for flake8",
    long_description=get_long_description(),
    keywords='pi naming',
    author='huang kh',
    author_email='561546441@qq.com',
    url='https://github.com/561546441/pi-naming.git',
    license='Expat license',
    py_modules=['pi_naming'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'N8 = pi_naming:NamingChecker',
        ],
        # Backward compatibility for Flint (now merged into Flake8)
        'flint.extension': [
            'N80 = pi_naming:NamingChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
