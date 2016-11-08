from setuptools import setup, find_packages
from codecs import open
import io
from os import path

here = path.abspath(path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(
    name = "yahoo_ff",
    version = "1.0.2",
    author = "Alexandre Sobolevski",
    author_email = "sobolevski.a@gmail.com",
    description = ("Quick module to scrape yahoo financial data for stocks."),
    license = "MIT",
    keywords = "yahoo financial data",
    url = "http://github.com/alexandresobolevski/yahoo_ff",
    packages=find_packages(exclude=['dist', 'docs']),
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
