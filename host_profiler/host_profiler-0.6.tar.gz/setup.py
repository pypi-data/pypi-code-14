# -*- coding: utf-8  -*-

from setuptools import setup

setup(name='host_profiler',
      version='0.6',
      description='get host informations',
      url='http://github.com/dowan/host_profiler',
      author='Dowan',
      author_email='contact@dowan.beer',
      license='MIT',
      scripts=['scripts/runbench'],
      packages=['host_profiler'],
      keywords = ['profiler', 'bench', 'psutil'],
      install_requires=['pandas', 'psutil'])
