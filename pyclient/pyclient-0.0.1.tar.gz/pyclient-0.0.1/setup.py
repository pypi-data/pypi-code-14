# coding: utf-8
import sys

from setuptools import setup

import pyclient


if sys.version_info[:2] == (3, 2):
    install_requires = ['requests<2.11.0']
else:
    install_requires = ['requests']


setup(
    name='pyclient',
    url='https://github.com/Stranger6667/pyclient',
    version=pyclient.__version__,
    packages=[],
    license='MIT',
    author='Dmitry Dygalo',
    author_email='dadygalo@gmail.com',
    maintainer='Dmitry Dygalo',
    maintainer_email='dadygalo@gmail.com',
    keywords=['python', 'api', 'client'],
    description='Building blocks for Python client libraries.',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    include_package_data=True,
    install_requires=install_requires,
)
