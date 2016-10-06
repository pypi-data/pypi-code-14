#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
   name='laws',
   version='0.0.2',
   description='Filter AWS instances',
   url='https://github.com/cyrillk/list-aws',
   author='Kirill Kulikov',
   author_email='kirill.kulikov@gmail.com',
   license='MIT',
   classifiers=[
    'License :: OSI Approved :: MIT License',
    'Environment :: Console'
   ],
   keywords=['aws', 'ec2'],
   packages=find_packages(),
   install_requires=['boto', 'tabulate']
)
