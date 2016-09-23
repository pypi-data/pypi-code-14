from setuptools import setup

setup(
    name='pybel-orca',
    packages=['pybel_orca'],
    version='0.2',
    py_modules=['bin/pybel-orca'],
    install_requires=[
        'Click',
        'openbabel',
    ],
    description = 'ORCA input file writer',
    author = 'Mohamad Mohebifar',
    author_email = 'mmohebifar@mun.ca',
    url = 'https://github.com/mohebifar/pybel-orca',
    download_url = 'https://github.com/mohebifar/pybel-orca/tarball/0.1',
    keywords = ['pybel-orca', 'rowley'],
    classifiers = [],
)
