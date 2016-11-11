# -*- coding: utf-8 -*-#
__author__ = 'tangrongjian'

import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup
"""
打包的用的setup必须引入，
"""


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "myjscss"
"""
名字，一般放你包的名字即可
"""

PACKAGES = ["myjscss"]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "this is a  package for package combine compress cache js,css to different client lib"
"""
关于这个包的描述
"""

LONG_DESCRIPTION = read("README.rst")
"""
参见read方法说明
"""

KEYWORDS = "combine compress cache js css"
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""

AUTHOR = "Tangrongjian"
"""
谁是这个包的作者，写谁的名字吧
"""

AUTHOR_EMAIL = "trj_2001@sina.com"
"""
作者的邮件地址
"""

URL = "http://pypi.python.org"
"""
你这个包的项目地址，如果有，给一个吧，没有你直接填写在PyPI你这个包的地址也是可以的
"""

VERSION = "1.0.6"
"""
当前包的版本，这个按你自己需要的版本控制方式来
"""

LICENSE = "MIT"
"""
授权方式，我喜欢的是MIT的方式，你可以换成其他方式
"""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=['pyScss', 'jsmin'],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
