from setuptools import setup, find_packages

setup(name='bees',
      version=0.01,
      description='Python package example',
      url='https://github.com/aarontuor/bees',
      author='Aaron Tuor',
      author_email='tuora@students.wwu.edu',
      license='none',
      packages=find_packages(), # or list of packages path from this directory
      zip_safe=False,
      install_requires=[],
      classifiers=['Programming Language :: Python'],
      keywords=['Package Distribution'])
