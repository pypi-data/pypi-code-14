"""A setuptools based setup module
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.dirname(__file__)

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='cvault',
        version='0.1.2',
        description='Credential Vault',
        long_description = long_description,
        url='https://github.com/starbops/cvault',
        author='Zespre Schmidt',
        author_email='starbops@zespre.com',
        license='MIT',
        platforms='any',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: End Users/Desktop',
            'Topic :: Utilities',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
        keywords='credential memo',
        packages=find_packages(exclude=['tests']),
        install_requires=['docopt'],
        entry_points={
            'console_scripts': [
                'cvault=cvault:main',
            ],
        },
)
