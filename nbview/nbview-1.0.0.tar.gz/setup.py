from setuptools import setup
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('nbview.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(name='nbview',
      version=version,
      author="Gouthaman Balaraman",
      author_email="gouthaman.balaraman@gmail.com",
      py_modules=['nbview'],
      install_requires = ['nbconvert', 'nbformat', 'ipython'],
      entry_points='''
      [console_scripts]
      nbview = nbview:main
      '''
      )