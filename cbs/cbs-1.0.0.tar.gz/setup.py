from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cbs',
    version='1.0.0',
    description='List coverage blind spots',
    long_description=long_description,

    url='https://github.com/christofsteel/cbs',
    download_url = 'https://github.com/christofsteel/cbs/tarball/1.0',

    author='Christoph Stahl',
    author_email='christoph.stahl@uni-dortmund.de',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    py_modules=["cbs"],
    install_requires=['h5py', 'numpy'],
    entry_points={
        'console_scripts': [
            'cbs=cbs:main',
        ],
    },
)
