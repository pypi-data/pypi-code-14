#!/usr/bin/python

from setuptools import setup

setup(name='Bohrium Pygments Lexer',
      version='0.0.1',
      description='Bohrium Pygments Lexer',
      license='GPL',
      author='Mads Ohm Larsen',
      author_email='ohm@nbi.ku.dk',
      packages=['bohrium_lexer'],
      install_requires=['pygments>=2.0.2'],
      url='https://github.com/bh107/bohrium_pygments_lexer',
      entry_points='''[pygments.lexers]
                      bohriumlexer = bohrium_lexer:BohriumLexer'''
)
