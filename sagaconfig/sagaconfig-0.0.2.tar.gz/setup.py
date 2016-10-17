from setuptools import setup
from io import open
import os

if not os.path.isfile('README.rst') and os.path.isfile('README.md'):
    with open('README.rst', 'w', encoding='utf-8') as readme:
        import pypandoc
        readme.write(pypandoc.convert('README.md', 'rst'))

long_description = open('README.rst').read()

setup(
    name='sagaconfig',
    packages=['sagaconfig'],
    package_dir={'sagaconfig': 'src'},
    version='0.0.2',
    description='A config helper',
    long_description=long_description,
    author='Sagacify',
    author_email='dev@sagacify.com',
    url='https://github.com/Sagacify/config-py',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ]
)
