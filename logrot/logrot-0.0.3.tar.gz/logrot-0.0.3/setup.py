from setuptools import setup, find_packages
import sys, os

version = '0.0.3'

setup(name='logrot',
      version=version,
      description="Receive piped output from a command and write it to a rotated file.",
      long_description="""Receive piped output from a command and write it to a rotated file.""",
      classifiers=[],
      keywords='log logging log-rotation',
      author='Jesse Aldridge',
      author_email='JesseAldridge@gmail.com',
      url='https://github.com/JesseAldridge/logrot',
      license='MIT',
      packages=[],
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      scripts=['scripts/logrot']
      )
