import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='travis_pypi_deploy_test',
    version='0.1',
    packages=['test_app'],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'django'
    ],
    description='Testing auto deplyoment to pypi via travis CI',
    long_description=README,
    author='Stephen De Vight',
    author_email='yourname@example.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)