#!/usr/bin/env python

from setuptools import setup
import clc_export_tool


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='clc-export-tool',
    version=clc_export_tool.__version__,
    author='CLC Analytics Team. #analytics',
    author_email='analytics@ctl.io',
    description='Elasticsearch data export tool',
    url='https://ctl.io/',


    packages=['clc_export_tool'],
    entry_points={'console_scripts': ['estool=clc_export_tool:main']},

    install_requires=['elasticsearch>=2.0.0,<3.0.0', 'argparse>=1.4.0', 'six>=1.10.0'],
    package_data={'': ['*.args']}
)
