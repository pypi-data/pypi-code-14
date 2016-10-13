#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from setuptools import setup, find_packages

VERSION = '0.2.1'

# with open('README.md') as f:
    # long_description = f.read()

setup(
      name='CryDeer', # 文件名
      version=VERSION, # 版本(每次更新上传Pypi需要修改)
      description="a command line express package helper",
      # long_description=long_description, # 放README.md文件,方便在Pypi页展示
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python express package helper', # 关键字
      author='vimsucks', # 用户名
      author_email='reg@vimsucks.com', # 邮箱
      url='https://github.com/vimsucks/CryDeer', # github上的地址,别的地址也可以
      license='GPLv3', # 遵循的协议
      packages=find_packages(), # 发布的包名
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests',
          'prettytable',
          'sqlalchemy',
          'sqlalchemy-utils',
      ], # 满足的依赖
      entry_points={
        'console_scripts':[
            'crydeer = CryDeer.crydeer:main'
        ]
      },
)
