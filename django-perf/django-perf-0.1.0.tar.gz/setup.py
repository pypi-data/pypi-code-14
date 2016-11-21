import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-perf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    license='LGPL-3.0',
    description='A simple Django Middleware for sending request data to Perf.',
    long_description=README,
    url='https://github.com/perflabs/django-perf',
    author='Jonathan Grana',
    author_email='john@perf.sh',
    classifiers=[],
)
