# coding=utf-8

from setuptools import setup
import re

with open('vcloudair/__init__.py') as f:
    v = re.search("^__version__ = '(.+?)'$", f.read(), re.MULTILINE)
    v = v.group(1)

if not v:
    raise RuntimeError('Cannot find version number')

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()
with open('CHANGELOG.rst', 'r', encoding='utf-8') as f:
    changelog = f.read()

setup(name='vcloudair',
      version=v,
      description='Python SDK for vCloud Air',
      long_description=readme+'\n\n'+changelog,
      author='Scott Schaefer',
      author_email='sschaefer@vmware.com',
      url='https://gitlab.com/scottjs/vcloudair',
      packages=['vcloudair'],
      install_requires=['requests>=2.10'],
      license='MIT',
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Systems Administration'
      ]
      )
