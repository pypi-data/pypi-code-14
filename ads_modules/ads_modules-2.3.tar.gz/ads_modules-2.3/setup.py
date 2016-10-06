"""
Installer for the ADS C modules.
"""

import os
import sys
from setuptools import setup, Extension

MODULES = ['Looker', 'ctrigram', 'ldw']

EXTENSIONS = [Extension(name=mod, sources=[mod + 'module.c'])
        for mod in MODULES]

setup (
     name         = "ads_modules",
     version      = "2.3",
     description  = "Looker and other modules for ADS system",
     author       = "Markus Demleitmer, Edwin Henneken",
     author_email = "ads@cfa.harvard.edu",
     url          = "http://adsabs.harvard.edu",
     test_suite   = "test",
     ext_modules  = EXTENSIONS,
)
