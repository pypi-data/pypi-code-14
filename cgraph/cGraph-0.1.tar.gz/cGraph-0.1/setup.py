from distutils.core import setup, Extension

cgraph_ext = Extension('cGraph', sources = ['graph.c'])

setup(
       name = 'cGraph',
       version = '0.1',
       description = 'Graph C extension with fast diameter computations.',
       ext_modules = [cgraph_ext]
       )

