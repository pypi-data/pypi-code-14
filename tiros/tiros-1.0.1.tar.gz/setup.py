"""Tiros, a VPC network analyzer"""

from setuptools import setup

setup(
    name='tiros',
    version='1.0.1',
    packages=['tiros'],
    install_requires=['requests>=2.11.1', 'boto3>=1.3.1', 'datetime>=4.1.1'],
    entry_points={
        'console_scripts': [
            'tiros = tiros:main',
        ],
    },
)
