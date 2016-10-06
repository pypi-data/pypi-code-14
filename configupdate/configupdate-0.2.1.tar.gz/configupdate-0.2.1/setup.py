#!/usr/bin/env python
import os
from distutils.core import setup

ldesc = ""

setup(name='configupdate',
      version="0.2.1",
      description='An utility to combine config files', 
      author='Carlos de Alfonso',
      author_email='caralla@upv.es',
      url='http://www.grycap.upv.es',
      scripts = [ "configupdate" ],
      license = "MIT",
      requires = [ 'cpyutils (>= 0.24)' ],
)
