# -*- coding: utf-8  -*-

from setuptools import setup
import os

def get_cwd():
    return os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))


def get_scripts():
    path = os.path.join(get_cwd(), 'scripts')
    scripts = []

    if os.path.exists(path):
        for root, _, files in os.walk(path):
            for f in files:
                scripts.append(os.path.join(root, f))

    return scripts


setup(name='host_profiler',
      version='0.3',
      description='get host informations',
      url='http://github.com/dowan/host_profiler',
      author='Dowan',
      author_email='contact@dowan.beer',
      license='MIT',
      scripts=get_scripts(),
      packages=['host_profiler'],
      keywords = ['profiler', 'bench', 'psutil'],
      requirements=['pandas>=0.71', 'psutil>=4.3.1'])
