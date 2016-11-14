import os
from setuptools import find_packages, setup

setup(
    name='django_site_health',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        "Django>=1.8",
    ],
    license='BSD License',
    include_package_data=True,
    description='A simple Django app to provide a health page for your site.',
    url='http://www.agogo.com/',
    author='Damian Hites',
    author_email='damian@agogo.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
