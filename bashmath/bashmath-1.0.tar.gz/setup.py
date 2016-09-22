"""
This will install bashmath on a new system. bashmath consists of a
set of scripts for basic math operations available from the command
line.
"""

from setuptools import setup

setup(
    name='bashmath',
    version='1.0',
    description='Handy utilities for tabular math in Bash',
    author="Piotr Mitros",
    author_email="piotr@mitros.org",
    url="https://github.com/pmitros/bash-math",
    packages=[
        'bashmath',
    ],
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'mean = bashmath.command_tools:mean',
            'median = bashmath.command_tools:median',
            'variance = bashmath.command_tools:variance',
            'stddiv = bashmath.command_tools:stddiv',
            'sumtotal = bashmath.command_tools:sumtotal'
        ]
    }
)
