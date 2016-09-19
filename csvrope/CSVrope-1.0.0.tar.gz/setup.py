try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
      name='CSVrope',
      version='1.0.0',
      license='Creative Commons Attribution 4.0 International license',
      author='thumbo',
	  author_email='',
      url='https://github.com/thumbo/CSVrope',
      install_requires=['nose'],
      packages=['csvrope'],
      description='A set of row-operations for CSV files.',
      keywords='csv edit utility row operation',
      long_description=open('README.rst').read(),
      )
