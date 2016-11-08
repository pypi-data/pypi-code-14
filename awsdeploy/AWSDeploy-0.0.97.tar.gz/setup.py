"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AWSDeploy',
    version='0.0.97',
    description='An AWS CodeDeploy preprocessor.',
    url='http://www.danielcreager.com/awsdeploy.html',
    author='Daniel R Creager',
    author_email='dan@danielcreager.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Pre-processors',
    ],
    entry_points={
        'console_scripts': [
            'deploy = com.danielcreager.Deploy:main',
        ],
    },
    keywords='setuptools development',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    package_data={'': ['__main__.py','license.html','profile.ini']},
    include_package_data=True,
    install_requires=['pip','boto3','botocore','PyYAML'],
    license='Apache License 2.0'
)

