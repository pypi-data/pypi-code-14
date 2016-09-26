import sys, os
from setuptools import setup

"""
Use pandoc to convert README.md to README.rst before uploading
   pandoc README.md -o README.rst
"""


if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


setup(
    name='piprot',
    version='0.9.7',
    author='Brenton Cleeland',
    author_email='brenton@brntn.me',
    packages=['piprot', 'piprot.providers'],
    url='http://github.com/sesh/piprot',
    license='MIT License',
    description='How rotten are your requirements?',
    long_description='',
    entry_points={
        'console_scripts': [
            'piprot = piprot.piprot:piprot',
        ]
    },
    install_requires=[
        'requests',
        'requests-futures',
        'six'
    ],
    classifiers=(
        b'Development Status :: 4 - Beta',
        b'Intended Audience :: Developers',
        b'Natural Language :: English',
        b'License :: OSI Approved :: MIT License',
        b'Programming Language :: Python',
        b'Topic :: Utilities',
        b'Programming Language :: Python :: 2.7',
        b'Programming Language :: Python :: 3',
        b'Programming Language :: Python :: 3.5',
    )
)
