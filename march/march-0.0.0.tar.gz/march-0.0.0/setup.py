#/usr/bin/env python
import io
from setuptools import setup
import sys


if sys.version_info[:3] < (3, 4):
    raise SystemExit("March requires Python 3.4+.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='march',
    version='0.0.0',
    description='An IDE suite for software development',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/',
    license='New BSD',
    install_requires=[
        'bugjar',
        'duvet',
        'cricket',
        'malcontent',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        # 'Operating System :: Microsoft :: Windows :: Windows 8',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
    ],
    test_suite='tests',
)
