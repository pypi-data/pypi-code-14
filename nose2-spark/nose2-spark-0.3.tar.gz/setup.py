from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nose2-spark',
    version='0.3',

    description='nose2 plugin to run the tests with support of pyspark.',
    long_description=long_description,
    url='https://github.com/malexer/nose2-spark',

    author='Alex (Oleksii) Markov',
    author_email='alex@markovs.me',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
    ],

    keywords=('nose2 spark pyspark unittest test'),

    packages=['nose2_spark'],
    install_requires=['nose2', 'findspark'],
)
