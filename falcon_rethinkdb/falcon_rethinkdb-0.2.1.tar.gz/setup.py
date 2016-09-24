import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = open("requirements.txt").read().strip().splitlines()
if sys.version_info.major != 3:
    raise EnvironmentError("only support python >= 3.4")
if sys.version_info.minor == 4:
    install_requires.append("typing")

setup(
    name='falcon_rethinkdb',
    version="0.2.1",
    packages=['falcon_rethinkdb'],
    url='https://github.com/lucidfrontier45/falcon_rethinkdb',
    license='Apache License version 2',
    author='Shiqiao Du',
    author_email='lucidfrontier.45@gmail.com',
    description='Falcon extension to easily use RethinkDB',
    install_requires=install_requires,
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
