# -*- coding: utf-8 -*-
from setuptools import setup


def _readme():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, 'README.rst')).read()


setup(
    name='make-clean',
    version=__import__('make_clean', fromlist=['__version__']).__version__,
    author='Tomohiro NAKAMURA',
    author_email='quickness.net@gmail.com',
    url='https://github.com/jptomo/make-clean.py',
    description='A Cleanup Utility',
    long_description=_readme(),
    py_modules=['make_clean'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
    entry_points={
        'console_scripts': [
            'make-clean = make_clean:main',
        ]
    },
    extras_require = {
        'test': ['pytest'],
        'pypi': ['wheel'],
    }
)
