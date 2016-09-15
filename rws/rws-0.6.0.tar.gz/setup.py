#!/usr/bin/env python

from setuptools import setup

setup(name='rws',
      version='0.6.0',
      description='Ranking Web Server',
      author='Algorithm Ninja',
      license='AGPL3',
      url='https://github.com/algorithm-ninja/rws',
      packages=[
          'cmsranking2',
          'cmsranking2.images',
          'cmsranking2.static',
          'cmsranking2.static.img',
          'cmsranking2.static.lib'
      ],
      package_data={
          '': ['*.svg', '*.js', '*.html', '*.css', '*.png', '*.ico']
      },
      install_requires=[
          'six',
          'gevent',
          'werkzeug',
          'json5',
      ],
      entry_points={
          'console_scripts': [
              'rws=cmsranking2.RankingWebServer:main',
          ]
      })
