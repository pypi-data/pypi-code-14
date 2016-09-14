#!/usr/bin/env python

from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name='Dajax',
        version='1.3',
        url='https://github.com/alexpirine/dajax',
        license='Public Domain',
        author='Alexandre Syenchuk',
        author_email='as@netica.fr',
        description='Django URL resolver for Ajax',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Django >= 1.9',
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Framework :: Django :: 1.9',
            'Framework :: Django :: 1.10',
            'Intended Audience :: Developers',
            'License :: Public Domain',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
