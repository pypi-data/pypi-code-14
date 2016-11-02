# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stamps-python',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.2',

    description='Stamps python SDK',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ui/stamps-python/',

    # Author details
    author='PT Stampindo Lancar Jaya',
    author_email='selwin@stamps.co.id',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='stamps API',
    packages=["stamps"],
    install_requires=['requests'],
    extras_require={
        'dev': [],  # See https://packaging.python.org/distributing/
        'test': [],
    },
    package_data={},
    data_files=[],
    entry_points={},
)
