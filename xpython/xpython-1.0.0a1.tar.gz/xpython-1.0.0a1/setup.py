"""
xPython
====================

**xPython** superset of Python language that can be converted to any other
language (Python, JavaScript, Java).


Quick start
-------------

Read `Quick Start <https://github.com/1st/xpython>`_ on GitHub.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = '1.0.0a1'


setup(
    name='xpython',
    version=version,
    url='https://github.com/1st/xpython',
    license='MIT',
    author='Anton Danilchenko',
    author_email='anton@danilchenko.me',
    description='xPython - compiles code to any other language.',
    keywords='python, compiler, xpython',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=[
        # 'xpython',
        # in future:
        # 'xpython.blocks',
    ],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    platforms='any'
)
