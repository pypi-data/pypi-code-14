from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name = "yangson",
    packages = ["yangson"],
    version = "1.0.0rc1",
    description = "Library for working with data modelled in YANG",
    long_description = long_description,
    url = "https://github.com/CZ-NIC/yangson",
    author = "Ladislav Lhotka",
    author_email = "lhotka@nic.cz",
    license = "LGPLv3",
    install_requires = ['PyXB'],
    tests_require = ["pytest"],
    keywords = ["yang", "data model", "configuration", "json"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Systems Administration"]
    )
