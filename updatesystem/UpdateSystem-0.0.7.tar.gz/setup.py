#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
import os,sys
from setuptools import setup,find_packages

version="0.0.7"
# from http://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()


setup(
    name = "UpdateSystem",          # 包名
    version = version,              # 版本信息
    packages = find_packages('lib'),  # 要打包的项目文件夹
    package_dir={ '': 'lib' },
    install_requires = [          # 安装依赖的其他包
    ],
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性
    scripts=[
         'bin/us',
    ],
    #url='www.xshalk.com',
    license='MIT',
    author='shalk',
    author_email='shalk@aliyun.com',
    description='update system '
)
