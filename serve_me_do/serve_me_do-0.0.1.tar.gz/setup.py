#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='serve_me_do',
    version='0.0.1',
    author='Felipe Lerena',
    author_email='felipelerena@gmail.com',
    packages=['serve_me_do'],
    scripts=[],
    url='http://pypi.python.org/pypi/serve_me_do/',
    license='WTFPL',
    description='command to serve some directory with multithreaded http server',
    long_description="",
    install_requires=[],
    entry_points={
        'console_scripts': ['serve_me_do = serve_me_do.__init__:run']
    },
)
