#!/usr/bin/env python
# _*_ coding=gbk _*_


from setuptools import setup, find_packages

setup(name='mcutool',
      version='1.0.2',
      description='a arm mcu debug tool',
      author='xwm',
      author_email='xwmdev@163.com',
      url='https://blog.xieweiming.cn',
      packages = find_packages(),
      #py_modules = ['Upgrade'],
      scripts = ['mcutool.py'],
      platforms = 'any',
      requires = ['wx','serial'],
     )