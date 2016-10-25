import codecs
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = 'user_behavior'
VERSION = '1.1.1'
DESCRIPTION = 'this is a test package for extract user behavior.'
LONG_DESCRIPTION = read('README.rst')
KEYWORDS = 'test user behavior'
AUTHOR = 'ma_k'
AUTHOR_EMAIL = 'ma_k@ctrip.com'
URL = 'https://github.com/mkloveyy/user_behaviors'
LICENSE = 'MIT'
PACKAGES = ['user_behavior']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
