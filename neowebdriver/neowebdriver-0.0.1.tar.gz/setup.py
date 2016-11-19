import sys
from setuptools import setup, find_packages


setup_args = {
    'name': 'neowebdriver',
    'packages': ['neowebdriver'],
    'version': '0.0.1',
    'description': 'WebDriver',
    'long_description': 'WebDriver',
    'url': 'https://github.com/lukas-linhart/neowebdriver',
    'author': 'Lukas Linhart',
    'author_email': 'lukas.linhart.1981@gmail.com',
    'license': 'MIT',
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: POSIX',
                    'Operating System :: MacOS :: MacOS X',
                    'Operating System :: Microsoft :: Windows',
                    'Topic :: Software Development :: Quality Assurance',
                    'Topic :: Software Development :: Testing',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.5'],
    'keywords': 'browser automation semantic WebDriver implementation',
    'packages': find_packages(exclude=['contrib', 'docs', 'tests*']),
}

setup(**setup_args)

