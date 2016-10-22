# -*- coding: utf-8 -*-

import sys
import os

currentDir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(currentDir, '..')))

os.chdir(currentDir)

import filesystem_crawler
import zipfile

with zipfile.ZipFile("root.zip","r") as zip_ref:
    zip_ref.extractall(".")