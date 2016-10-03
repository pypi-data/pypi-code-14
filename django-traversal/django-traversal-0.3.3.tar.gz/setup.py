from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='django-traversal',
    version='0.3.3',
    author=str('WhiteMasteR'),
    author_email=str('whthaker@gmail.com'),
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=(str('Django<=1.10'),),
    test_suite='tests',
    classifiers=[
        str('Development Status :: 4 - Beta'),
        str('Environment :: Web Environment'),
        str('Framework :: Django'),
        str('Intended Audience :: Developers'),
        str('License :: OSI Approved :: MIT License'),
        str('Operating System :: OS Independent'),
        str('Programming Language :: Python'),
        str("Programming Language :: Python :: 2"),
        str("Programming Language :: Python :: 2.6"),
        str("Programming Language :: Python :: 2.7"),
        str("Programming Language :: Python :: Implementation :: CPython"),
        str('Topic :: Utilities'),
    ],
)
