from setuptools import find_packages
from setuptools import setup


setup(name='binpacker',
      version='0.1.3',
      description='Distribute weighted tasks equally to workers by solving Bin Packing problem. This package provides an abstraction for user to extend',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4'
      ],
      keywords='algorithm bin packing shipping inventory warehouse transportation distribution parallel',
      url='https://github.com/pkuong/binpacker',
      author='Paulo Kuong',
      author_email='paulo.kuong@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
