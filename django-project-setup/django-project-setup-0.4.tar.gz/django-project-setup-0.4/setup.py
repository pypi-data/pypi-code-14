import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-project-setup',
    version='0.4',
    scripts=['django_project_setup'],
    packages=find_packages(),
    include_package_data=True,
    license='FREE',  # example license
    description='A simple python script to setup django project easily',
    long_description=README,
    url='http://www.maneeshvshaji.in/',
    author='Maneesh',
    author_email='maneeshvettukattil@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
