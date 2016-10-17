""" this script is design for dagobah"""
# _*_ coding: utf-8 _*_

from distutils.core import setup
from setuptools import find_packages

setup(
        name = "niiu",
        packages = find_packages(),
        version = "0.8.9",
        classifiers = [
            "Programming Language :: Python",
            ],
	scripts = [
                "bin/funnist-joke",
                "bin/lala.sh",
                "niiu/niiu.py",
                "niiu/nana.py"
    	    ]
    )
