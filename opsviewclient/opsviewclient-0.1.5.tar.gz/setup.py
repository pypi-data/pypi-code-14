#!/usr/bin/env python
# coding: utf-8

import setuptools

try:
    import multiprocessing
except ImportError:
    pass

setuptools.setup(setup_requires=['pbr>=1.8'], pbr=True)

# from distutils.core import setup
#
# setup(
#     name='opsviewclient',
#     packages=['opsviewclient'],
#     version='0.1.1',
#     description='API client for interacting with the Opsview API',
#     author='Joshua Griffiths',
#     author_email='jgriffiths@ceramyq.com',
#     url='https://github.com/jgriffiths1993/python-opsviewclient',
#     download_url='https://github.com/jgriffiths1993/python-opsviewclient/tarball/0.1.1',
#     keywords=['opsview'],
#     classifiers=[]
# )
