import sys
from setuptools import setup, find_packages

__version__ = '0.25.1'
__author__ = 'Barcelona Biomedical Genomics Lab'

if sys.hexversion < 0x03000000:
    raise RuntimeError('This package requires Python 3.0 or later.')

setup(
    name="bgdata",
    version=__version__,
    packages=find_packages(),
    author=__author__,
    description="Simple data repository managment.",
    license="Apache License 2",
    keywords=["data", "managment", "repository"],
    url="https://bitbucket.org/bgframework/bgdata",
    download_url="https://bitbucket.org/bgframework/bgdata/get/"+__version__+".tar.gz",
    install_requires=['bgconfig >= 0.2.0', 'homura >= 0.1.3'],
    classifiers=[],
    package_data={'': ['*.template', '*.template.spec']},
    entry_points={
        'console_scripts': [
            'bg-data = bgdata.utils:cmdline',
            'bgdata = bgdata.utils:cmdline'
        ]
    }
)
