# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as stream:
    long_desc = stream.read()


version = "0.16"
requires = [
    'path.py',
    'simplejson',
    'Sphinx >= 1.0b2',
    'erppeek',
    ]
extra_require = {
    }

setup(
    name='odoodoc',
    version=version,
    url='https://github.org/minorisa/odoodoc',
    download_url='http://pypi.python.org/pypi/odoodoc',
    license='BSD',
    author='Minorisa, S.L.',
    author_email='projectes.odoo@minorisa.net',
    description='Odoo markup for Sphinx',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    entry_points={},
    install_requires=requires,
    extras_require=extra_require,
    namespace_packages=['sphinxcontrib'],
    use_2to3=True,
)
