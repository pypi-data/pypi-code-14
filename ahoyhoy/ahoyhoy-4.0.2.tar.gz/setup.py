import os
from setuptools import setup, find_packages


with open('docs/PYPI_README.rst') as readme:
    README = readme.read()

REQUIREMENTS = [i.strip() for i in open('requirements/base.txt').readlines()]

setup(
    name='ahoyhoy',
    version=os.environ.get('VERSION', ''),
    packages=find_packages(exclude=('tests')),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    license='Public Domain',
    description="Python client for service requests",
    long_description=README,
    url='http://www.ncbi.nlm.nih.gov/',
    author='NCBI',
    author_email='python-core@ncbi.nlm.nih.gov',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='python web requests client'
)
