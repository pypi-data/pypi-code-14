"""Setup module for google-api-wrapper

See:
https://bitbucket.org/infolinks/google-api-wrapper
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='google-api-wrapper',
    version='1.0.0b2',
    description='Simple wrapper for Google APIs',
    long_description=long_description,
    url='https://bitbucket.org/infolinks/google-api-wrapper',
    author="Arik Kfir",
    author_email="arik@infolinks.com",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.5',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration"
    ],
    keywords=["google", "cloud", "api", "wrapper", "compute", "iam", "deployment"],
    packages=find_packages(where='src', exclude=['contrib', 'docs', 'tests']),
    package_dir={'': 'src'},
    install_requires=['google-api-python-client']
)
