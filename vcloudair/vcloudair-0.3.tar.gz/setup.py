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
      classifiers=(
          b'Development Status :: 3 - Alpha',
          b'Intended Audience :: Developers',
          b'Natural Language :: English',
          b'License :: OSI Approved :: MIT License',
          b'Operating System :: MacOS',
          b'Operating System :: Microsoft :: Windows',
          b'Operating System :: POSIX :: Linux',
          b'Programming Language :: Python :: 3',
          b'Programming Language :: Python :: Implementation :: CPython',
          b'Topic :: Software Development :: Libraries :: Python Modules'
      )
      )
