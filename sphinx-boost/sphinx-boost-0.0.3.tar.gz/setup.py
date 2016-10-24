from setuptools import setup, find_packages

from sphinx_boost import __version__

setup(
    name="sphinx-boost",
    version=__version__,
    url='https://github.com/pfultz2/sphinx-boost',
    license='boost',
    description='Boost theme for sphinx',
    author='Paul Fultz II',
    author_email='pfultz2@yahoo.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
