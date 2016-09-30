from distutils.core import setup

from setuptools import find_packages

setup(
    name = 'adaptivepy',
    packages = find_packages(),
    version = '0.1.2',
    description = 'Design patterns for easy addition of adaptive behavior in an '
                'extensible and testable way.',
    author = 'Samuel Longchamps',
    author_email = 'samuel.longchamps@usherbrooke.ca',
    url = 'https://gitlab.com/memophysic/adaptive_py_lib',
    download_url = 'https://gitlab.com/memophysic/adaptive_py_lib/repository/archive.tar.gz?ref=0.1.2',
    keywords = ['adaptive', 'monitor', 'proxy', 'router', 'component'],
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved',
        'Topic :: Adaptive Technologies',
        'Development Status :: 3 - Alpha'
    ],
)
