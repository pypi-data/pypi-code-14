#! /usr/bin/env python

import sys
from setuptools import setup


if 'upload' in sys.argv:
    if '--sign' not in sys.argv and sys.argv[1:] != ['upload', '--help']:
        raise SystemExit('Refusing to upload unsigned packages.')


pkg = 'concon'


setup(
    name=pkg,
    description='CONstrained CONtainers: immutable & append-only containers.',
    url='https://github.com/nejucomo/{}'.format(pkg),
    license='MIT (see LICENSE.txt)',
    version='2.0.1',
    author='Nathan Wilcox',
    author_email='nejucomo@gmail.com',
    py_modules=[pkg],
)
