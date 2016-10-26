import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='juta-icons',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='New Icon Admin Field.',
    long_description=README,
    url='http://double-eye.com/',
    author='Double Eye',
    author_email='info@double-eye.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)


with open(os.path.join(os.path.dirname(__file__), 'DELICENSE.txt')) as license_print:
    message = license_print.read()
    print message.encode('ascii', 'ignore')

