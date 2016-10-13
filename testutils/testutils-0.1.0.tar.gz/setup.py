from setuptools import setup, find_packages

long_description = 'handy utilities for testing and automation prototyping'

setup_args = {
    'name': 'testutils',
    'version': '0.1.0',
    'description': 'testing and automation utilities',
    'long_description': long_description,
    'url': 'https://github.com/lukas-linhart/testutils',
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
    'keywords': 'testutils testing automation prototyping utils utilities',
    'packages': find_packages(exclude=['contrib', 'docs', 'tests*']),
    'install_requires': ['selenium>=2.53.0']
}

setup(**setup_args)

