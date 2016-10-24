# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='i18nize',
    version='0.0.1',
    author=u'Mohammed Hammoud',
    author_email='mohammed@iktw.se',
    packages=find_packages(),
    url='https://github.com/iktw/i18nize',
    license='MIT licence, see LICENCE.txt',
    description='This is a simple Client that integrates with the localization service www.i18nize.com',
    long_description=open('README.md').read(),
    zip_safe=False,
    include_package_data=True
)