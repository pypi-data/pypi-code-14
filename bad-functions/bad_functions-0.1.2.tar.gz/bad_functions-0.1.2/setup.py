from setuptools import setup
from distutils.core import Extension

bad_functions_module = Extension('bad_functions', sources=['bad_functions/funcs_module.c', 'bad_functions/funcs.c'])
setup(name='bad_functions',
      version='0.1.2',
      description='Set of bad functions in C that cause bad behavior',
      py_modules=['bad_functions.dummy'],
      ext_modules=[bad_functions_module])
