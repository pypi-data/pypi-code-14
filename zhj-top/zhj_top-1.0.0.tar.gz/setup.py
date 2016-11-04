#coding=utf8
from setuptools import setup, find_packages

setup(
    name='zhj_top',

    version='1.0.0',

    description="taobao openapi interface",

    long_description="",

    url="https://pypi.python.org/pypi/zhj_top/",

    author="taobao Team",

    author_email="zhongjin616@foxmail.com",

    license='',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='taobao openapi',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    install_requires=[],

    # List additional groups of dependencies here
    extras_require={},
)