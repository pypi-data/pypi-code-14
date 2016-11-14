"""
# Flask-Mage2Connector
=====================

## Synopsis
The python flask extension is used to connect the Magento 2 with MySQL connection and RESTful api to perform all of the data related functions.

## Configuration

#### MAGE2DBSERVER
Magento 2 MySQL DB Server full DNS name or IP address.

#### MAGE2DBUSERNAME
Magento 2 MySQL username.

#### MAGE2DBPASSWORD
Magento 2 MySQL password.

#### MAGE2DB
Magento 2 MySQL database name.
"""
from setuptools import find_packages, setup

setup(
    name='Flask-Mage2Connector',
    version='0.0.1',
    url='https://github.com/ideabosque/Flask-Mage2Connector',
    license='MIT',
    author='Idea Bosque',
    author_email='ideabosque@gmail.com',
    description='Use to connect Magento 2.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['requests', 'Flask', 'MySQL-python',],
    download_url = 'https://github.com/ideabosque/Flask-Mage2Connector/tarball/0.0.1',
    keywords = ['Magento 2'], # arbitrary keywords
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
