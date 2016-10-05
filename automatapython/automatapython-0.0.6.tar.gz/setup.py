#!/usr/bin/env python
"""Setup logic for pip."""

from setuptools import setup


def get_long_description():
    """Get long description used on PyPI project page."""
    try:
        # Use pandoc to create reStructuredText README if possible
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except:
        return None


setup(
    name='automatapython',
    version='0.0.6',
    description='The only automaton library you will ever need',
    long_description=get_long_description(),
    url='https://github.com/hemangsk/automatapython',
    author='Hemang Kumar',
    author_email='hemangsk@gmail.com',
    license='GPLv3',
    keywords='language finite automata turing machine push down automata linear bound automata',
    packages=[
        'automata'
    ],
    install_requires=[],
    entry_points={}
)
