# -*- encoding: utf-8 -*-

import os
import sys
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

setup(
    name='django-polybuilder',
    version='0.2.2',
    packages=['polybuilder'],
    install_requires=[
        'Django',
    ],
    include_package_data=True,
    license='MIT License',
    description='Create your own Web Components from Django admin.',
    long_description=README,
    author='Sparsy',
    author_email='sparsyteam@gmail.com',
    url='https://sunetraalex@bitbucket.org/sparsy/django-polybuilder',
    download_url='https://bitbucket.org/sparsy/django-polybuilder/get/v_0.2.2.zip',
    keywords=[
        'django', 'polymer', 'admin', 'editor', 'webcomponents'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
