import os

from setuptools import setup

# Using vbox, hard links do not work
if os.environ.get('USER','') == 'vagrant':
    del os.link

setup(
    name='closet',
    version='0.1.5',
    description='File storage abstraction',
    long_description='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],
    url='https://github.com/BasementCat/closet',
    author='Alec Elton',
    author_email='alec.elton@gmail.com',
    license='',
    packages=['closet'],
    install_requires=['python-magic'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)