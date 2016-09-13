#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
  import setuptools
  from setuptools import setup, find_packages
except ImportError:
  print("Please install setuptools.")

def find_scripts(scripts_path):
  base_path = os.path.abspath(scripts_path)
  return list(map(lambda path: os.path.join(scripts_path, path), 
           filter(lambda file_name: os.path.isfile(
             os.path.join(base_path, file_name)), os.listdir(base_path)
         )))

import os
import sys

libdir = "rita"

sys.path.insert(0, libdir)

import info
import version

setup_options = info.INFO
setup_options["version"] = version.VERSION
setup_options.update(dict(
  packages         = ["rita","rita.misc","rita.misc.session","rita.misc.controller"]
  ,package_dir         = {"":"lib"}
))

#print(find_packages(libdir))
setup(**setup_options)
