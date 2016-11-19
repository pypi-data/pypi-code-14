# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.7.30'

setup(name='pygments-ccl-lexer',
      version=version,
      description='Pygments lexer for CCL',
      long_description=open('README.rst').read(),
      keywords='pygments ccl lexer',
      author='Thomas J. Perry',
      author_email='admin@daftscience.com',
      url='https://github.com/daftscience/pygments-ccl-lexer',
      license='GPL',
      packages=find_packages(),
      install_requires=[
          'pygments >= 1.4',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
        [pygments.lexers]
        ccl=ccl_lexer:CCL_Lexer
    """,
      )
