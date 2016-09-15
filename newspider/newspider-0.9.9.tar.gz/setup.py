# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="newspider",
    version="0.9.9",
    description="分类扒数据的简易框架",
    long_description="",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=(""),
    author="Ray",
    author_email="miuyin@126.com",
    url="http://www.typechodev.com",
    license="MIT",
    packages=['newspider','newspider.comm'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['threadpool', 'pyquery', 'requests'],
    platforms="any"
)
