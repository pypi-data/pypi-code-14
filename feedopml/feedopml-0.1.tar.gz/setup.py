"""
    setup
    ~~~~~

    :copyright: 2016 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""

from setuptools import setup


setup(
    name='feedopml',
    version='0.1',
    url='https://github.com/DasIch/feedopml',
    author='Daniel Neuhäuser',
    author_email='ich@danielneuhaeuser.de',
    install_requires=['lxml'],
    py_modules=['feedopml']
)
