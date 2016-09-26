#-*- coding:utf-8 -*-
import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
	name="tran",
	version="1.0",
	description="方便在终端中译英和英译中的小工具",
	classifiers=[],
	keywords="python terminal",
	author="kakit",
	author_email="kakitgo@gmail.com",
	url="https://github.com/kakitgogogo/Translator",
	packages=['tran',],
	entry_points={
        'console_scripts':[
            'tran = tran.tran:main'
        ]
      },
)
