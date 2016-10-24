from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gbboxcli',
    version='0.2.1',
    description='Command-line interface for gbbox',
    long_description=long_description,
    url='https://github.com/boxnwhiskr/gbboxcli',
    author='-[|]- Box and Whisker',
    author_email='box@boxnwhis.kr',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',

        'License :: OSI Approved :: MIT License',

        'Natural Language :: English',

        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',

        'Topic :: Games/Entertainment',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='testing experiment optimization gbbox',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['click', 'requests', 'PyYAML', ],

    extras_require={
        'dev': [],
        'test': ['coverage', 'nose', ],
    },

    test_suite='nose.collector',

    package_data={
        # 'sample': ['package_data.dat'],
    },

    entry_points={
        'console_scripts': [
            'gbboxcli=gbboxcli.cli:main',
        ],
    },
)
