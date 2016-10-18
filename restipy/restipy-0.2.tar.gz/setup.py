from setuptools import setup, find_packages

setup(
    version='0.2',
    name='restipy',
    description=
        '''
            Core Restipy library. This library basically uses Jinja2 and the requests
            library to build dynamic requests based on a template
        ''',
    author='Phil Hachey',
    author_email='phil.hachey@bluespurs.com',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.11',
        'pyyaml >= 3.12',
        'python-jose >= 1.3',
        'jinja2 >= 2.8'
    ]
)
