#!/usr/bin/env python3
#coding=utf-8

import os
import sys
import ast
from setuptools import setup

path = os.path.dirname(os.path.realpath(__file__))

class DictionaryRef(object):
    def __init__(self, d, k, l):
        self.dictionary = d
        self.key = k
        self.func = l
    def value(self):
        return self.func(self.dictionary[self.key].m_value)

class DictionaryVal(object):
    def __init__(self, v):
        self.m_value = v
    def value(self):
        return self.m_value;

def get_version(file):
    with open(file) as infile:
        for line in infile:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s

def get_short_description(file):
    with open(file) as infile:
        for line in infile:
            if line.startswith('__description__'):
                return ast.parse(line).body[0].value.s

def get_long_description(file):
    try:
        with open('README.md', 'r') as infile:
            return infile.read()
    except IOError:
        return get_short_description(file)

properties = {}
properties.update({
    "Package Name": DictionaryVal("just_solve_10"),
    "Version": DictionaryRef(properties, "Package Name", l = lambda x: get_version(path+"/"+x+".py")),
    "Short Description": DictionaryRef(properties, "Package Name", l = lambda x: get_short_description(path+"/"+x+".py")),
    "Long Description": DictionaryRef(properties, "Package Name", l = lambda x: get_long_description(path+"/"+x+".py"))
})

setup(
    name=properties["Package Name"].value(),
    version=properties["Version"].value(),
    author='Ian Oltuszyk',
    author_email='ian.oltu@gmail.com',
    description=properties["Short Description"].value(),
    url='https://github.com/ioltuszyk/just-solve-10',
    long_description=properties["Long Description"].value(),
    py_modules=[properties["Package Name"].value()],
    entry_points={
        'console_scripts': [
            'just_solve_10 = just_solve_10:main'
        ]
    },
    license='MIT License'
)