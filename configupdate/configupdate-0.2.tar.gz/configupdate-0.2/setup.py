#!/usr/bin/env python
import os
from distutils.core import setup

ldesc = ""
f = open("README.md","rt")
ldesc = f.read()
f.close()

setup(name='configupdate',
      version="0.2",
      description='An utility to combine config files', 
      author='Carlos de Alfonso',
      author_email='caralla@upv.es',
      url='http://www.grycap.upv.es',
      scripts = [ "configupdate" ],
      long_description=ldesc,
      license = "MIT",
      requires = [ 'cpyutils (>= 0.24)' ],
)
