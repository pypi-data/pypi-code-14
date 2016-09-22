# -*- coding: utf-8  -*-

from setuptools import setup
import os

setup(name='host_profiler',
      version='0.4',
      description='get host informations',
      url='http://github.com/dowan/host_profiler',
      author='Dowan',
      author_email='contact@dowan.beer',
      license='MIT',
      scripts=[
        'scripts/runbench.py'
      ],
      packages=['host_profiler'],
      keywords = ['profiler', 'bench', 'psutil'],
      requirements=['pandas>=0.71', 'psutil>=4.3.1'])
