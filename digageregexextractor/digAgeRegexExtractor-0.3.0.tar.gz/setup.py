
from distutils.core import setup
from setuptools import find_packages

setup(
    name='digAgeRegexExtractor',
    version='0.3.0',
    description='digAgeRegexExtractor',
    author='Jason Slepicka',
    author_email='jasonslepicka@gmail.com',
    url='https://github.com/usc-isi-i2/dig-age-regex-extractor',
    download_url='https://github.com/usc-isi-i2/dig-age-regex-extractor',
    packages=find_packages(),
    keywords=['age', 'extractor'],
    install_requires=['digExtractor', 'digRegexExtractor']
)
