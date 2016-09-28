from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()


REQUIREMENTS = [
    'requests'
]


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

setup(name='hackerrank-sdk',
      version='1.2.1',
      description='Python client for HackerRank API',
      long_description=long_description,
      url='https://github.com/nikhilkumarsingh/hackerrank-sdk',
      author='Nikhil Kumar Singh',
      author_email='nikhilksingh97@gmail.com',
      license='MIT',
      packages=['hackerrank'],
      classifiers=CLASSIFIERS,
      keywords='hackerrank code compiler online api python client',
      )
