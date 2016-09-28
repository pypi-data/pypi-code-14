#!/usr/bin/env python
# _*_ coding=gbk _*_


from setuptools import setup, find_packages

setup(name='mcutool',
    version='1.0.6',
    description='a arm mcu debug tool',
    author='xwm',
    author_email='xwmdev@163.com',
    url='https://blog.xieweiming.cn',
    packages = find_packages(),
    #scripts = ['mcutool.py'],
    platforms = 'any',
    requires = ['wx','serial'],
    entry_points={
        "console_scripts": [
        "mcutool=mcutools:main",
        #"pip%s=pip:main" % sys.version[:1],
        #"pip%s=pip:main" % sys.version[:3],
        ],
    },
    zip_safe=False,
    )