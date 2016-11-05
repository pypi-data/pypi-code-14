# -*- coding: utf-8 -*-

import re
import ast

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def extract_version():
    with open('exp100/__init__.py', 'rb') as f_version:
        ast_tree = re.search(
            r'__version__ = (.*)',
            f_version.read().decode('utf-8')
        ).group(1)
        if ast_tree is None:
            raise RuntimeError('Cannot find version information')
        return str(ast.literal_eval(ast_tree))

with open('README.rst', 'rb') as f_readme:
    readme = f_readme.read().decode('utf-8')

packages = ['exp100']

version = extract_version()

setup(
    name='exp100',
    version=version,
    keywords=['internet', 'query', 'express', 'http'],
    description='I\'m a small script that help you get '
                'express package information use kuaidi100.com api.',
    long_description=readme,
    author='Chris',
    author_email='luohuawoaini@gmail.com',
    license='MIT',
    url='http://www.iloveplum.in/',

    install_requires=[],
    packages=packages,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Information Technology',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],

    entry_points={
        'console_scripts': [
            'exp100 = exp100.exp100:main'
        ]
    }
)
