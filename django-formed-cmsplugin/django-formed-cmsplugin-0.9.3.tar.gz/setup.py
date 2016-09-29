# coding=utf-8
from __future__ import unicode_literals
from setuptools import setup, find_packages
import os

version = __import__('cmsplugin_formed_form').__version__


def read(file_name):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='django-formed-cmsplugin',
    packages=find_packages(),
    version=version,
    url='https://bitbucket.org/frontendr/django-formed-cmsplugin',
    license='MIT',
    platforms=['OS Independent'],
    description="A DjangoCMS plugin which allows you to add a form created with django-formed to your page.",
    long_description=read('README.rst'),
    keywords='DjangoCMS formed plugin',
    author='Johan Arensman',
    author_email='johan@frontendr.com',
    install_requires=(
        'Django>=1.8,<1.9.999',  # Django is known to use rc versions
        'django-formed>=0.9.10',
        'django-cms>=3.3.2,<4',
    ),
    include_package_data=True,
    zip_safe=True,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
    ],
)
