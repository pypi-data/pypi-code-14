from setuptools import setup, Extension

hello_world_module = Extension('hello_module', sources=['hello_module.c'])

setup(name='miscpy',
      version='0.2.13',
      description='miscpy facilitates (scientific) python scripting. It facilitates file and  data handling through various miscellaneous functions and missing data structures.',

      ext_modules=[hello_world_module],
      packages=['miscpy', 'miscpy/DataStructure'],

      url='https://github.com/manuSrep/miscpy.git',
      author='Manuel Tuschen',
      author_email='Manuel_Tuschen@web.de',
      license='FreeBSD License',
      zip_safe=False)
