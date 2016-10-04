from setuptools import setup, Extension

setup(name='miscpy',
      version='0.2.18',
      description='miscpy facilitates (scientific) python scripting. It facilitates file and  data handling through various miscellaneous functions and missing data structures.',

      ext_modules=[Extension('miscpy.hello_module', sources=['miscpy/hello_module.c'])],
      packages=['miscpy', 'miscpy.DataStructure'],
      url='https://github.com/manuSrep/miscpy.git',
      author='Manuel Tuschen',
      author_email='Manuel_Tuschen@web.de',
      license='FreeBSD License')
