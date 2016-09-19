"""Installer for trestus
"""

import os
from setuptools import setup, find_packages


setup(
    name='trestus',
    description='Static status page generator that uses a Trello board as a '
                'data source',
    long_description=open('README.rst').read(),
    version='1.0.2',
    author='Wes Mason',
    author_email='wesley.mason@canonical.com',
    url='http://canonical-ols.github.io/trestus/',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=open(
        os.path.join(os.path.dirname(__file__),
            'requirements.txt')).readlines(),
    package_data={'trestus': ['templates/trestus.html',
                              'templates/trestus.css']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'trestus = trestus.__init__:main',
        ],
    },
    license='AGPL3',
    classifiers=[
        "Topic :: System :: Networking",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Affero General Public License v3 or"
            " later (AGPLv3+)",
    ]
)
