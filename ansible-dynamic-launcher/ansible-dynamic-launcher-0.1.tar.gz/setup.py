#! /usr/bin/env python
#################################################################################
#     File Name           :     setup.py
#     Created By          :     jonesax
#     Creation Date       :     [2016-11-19 14:11]
#     Last Modified       :     [2016-11-19 14:24]
#     Description         :     Installer 
#################################################################################

from setuptools import setup

setup(
    name='ansible-dynamic-launcher',
    version='0.1',
    url="https://github.com/AlexsJones/ansible-dynamic-launcher.git",
    packages=['ansible-dynamic-launcher'],
    install_requires=['ansible','Jinja2','python-nmap','PyYAML','configobj','markupsafe'],
    author="Alex Jones",
    author_email="tibbar@freedommail.ch"
)
