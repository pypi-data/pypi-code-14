from setuptools import find_packages
from setuptools import setup


setup(name='knapsack01',
      version='0.0.1',
      description='Solving 0/1 Knapsack Problem',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4'
      ],
      keywords='algorithm knapsack',
      url='https://github.com/pkuong/knapsack01',
      author='Paulo Kuong',
      author_email='paulo.kuong@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
