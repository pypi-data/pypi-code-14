#!env/bin/python
from setuptools import setup, find_packages

license_type = 'MIT License'
dev_status = '3 - Alpha'
# dev_status = '4 - Beta'
# dev_status = '5 - Production/Stable'

setup(

    # Author
    author='Astafev Alexey',
    author_email='efsneiron@gmail.com',

    # Meta
    name='alt-bucket',
    version='0.0.2',
    description='The common package',
    url='https://github.com/altaid/bucket',
    keywords=[
        'python3',
        'flask',
        'orm',
        'sqlalchemy',
        'webapp'
    ],

    # classifiers
    # see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # Development status
        'Development Status :: ' + dev_status,
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        # License
        'License :: OSI Approved :: ' + license_type,

        # categories
        'Programming Language :: Python :: 3',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],

    # Project packages
    packages=find_packages(exclude=['tests*']),

    # include none-code data files from manifest.in (http://goo.gl/Uf0Yxc)
    include_package_data=True,

    # project dependencies
    install_requires=[],

    # entry_points={
    #     'console_scripts': [
    #         'bucket=bucket:main',
    #     ],
    # },

    # License
    license=license_type,
)
