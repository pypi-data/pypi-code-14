from setuptools import setup
from pip.req import parse_requirements
from os import path
from codecs import open

with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='buku',
    version='0.0.7',
    description='Powerful command-line bookmark manager. Your mini web!',
    long_description=long_description,
    url='https://github.com/jarun/Buku',
    author='Jarun',
    author_email='ovv@outlook.com',
    license='GPLv3',
    packages=['buku'],
    include_package_data=True,
    package_data={'auto-completion': ['bash/*', 'fish/*', 'zsh/*']},
    entry_points={
        'console_scripts': ['buku=buku.buku:entry_point']
    },
    install_requires=['beautifulsoup4>=4.4.1', 'cryptography>=1.3.2'],
)
