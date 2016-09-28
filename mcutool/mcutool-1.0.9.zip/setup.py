#!/usr/bin/env python
# _*_ coding=gbk _*_


from setuptools import setup, find_packages

setup(name='mcutool',
    version='1.0.9',
    description='a arm mcu debug tool',
    author='xwm',
    author_email='xwmdev@163.com',
    url='https://blog.xieweiming.cn',
    license='BSD License',
    packages = find_packages(),
    #platforms = 'any',
    install_requires = ['pyserial'],
    entry_points={
        "console_scripts": ["mcutool=mcutools:main"],
    },
    zip_safe=False,
    include_package_data=True,
    )