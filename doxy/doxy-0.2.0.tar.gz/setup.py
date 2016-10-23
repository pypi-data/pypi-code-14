#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
setup(name='doxy',
      version='0.2.0',
      description='Doxy is a simple wrapper over doxygen to generate multiple documentation for c++ library',
      long_description=readme(),
      url='http://github.com/HeeroYui/doxy',
      author='Edouard DUPIN',
      author_email='yui.heero@gmail.com',
      license='APACHE-2',
      packages=['doxy'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Compilers',
      ],
      keywords='documentation over doxygen',
      scripts=['bin/doxy'],
      # Does not work on MacOs
      #data_file=[
      #    ('/etc/bash_completion.d', ['bash-autocompletion/lutin']),
      #],
      include_package_data = True,
      zip_safe=False)

#To developp: sudo ./setup.py install
#             sudo ./setup.py develop
#TO register all in pip: ./setup.py register sdist upload

