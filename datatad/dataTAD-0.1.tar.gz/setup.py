
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='dataTAD',
      version='0.1',
      description='A module with sample data to learn Text as Data for Social Science Research',
      url='http://andreucasas.com/text_as_data/',
      author='Andreu Casas',
      author_email='acasas2@uw.edu',
      license='MIT',
      packages=['dataTAD'],
      install_requires=[],
      zip_safe=False,
      include_package_data=True)