from setuptools import setup

setup(
    name='pbs-generator',
    packages=['pbs_generator'],
    version='1.2',
    entry_points = {
        'console_scripts': ['nicesub=pbs_generator.cli:ssh'],
    },
    install_requires=['Click', 'tabulate', 'paramiko'],
    description = 'A PBS script generator',
    author = 'Mohamad Mohebifar',
    author_email = 'mmohebifar@mun.ca',
    url = 'https://github.com/RowleyGroup/pbs-generator',
    download_url = 'https://github.com/RowleyGroup/pbs-generator/tarball/1.0',
    keywords = ['pbs-generator', 'rowley'],
    classifiers = [],
)
