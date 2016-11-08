# -*- coding: utf-8 -*-
import codecs
import os

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

def read(fname):
    """
    定义一个read方法，用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

PACKAGE = "djdg_common_verify"
NAME = "djdg_python_common_verify_SDK"
DESCRIPTION = "djdg common verify"
AUTHOR = "fredzhang"
AUTHOR_EMAIL = "slzhang08@qq.com"
URL = "https://pypi.python.org/pypi/djdg-common-verify"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 2',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    install_requires=['django', 'djangorestframework', 'requests'],
    zip_safe=False,
)
