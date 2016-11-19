from setuptools import setup


NAME = "itzpip"

PACKAGES = ["itzpip",]

DESCRIPTION = "itz libs"

KEYWORDS = "itz"

AUTHOR = "XinLi"

AUTHOR_EMAIL = "lixin@itouzi.com"

VERSION = "0.0.4"

LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)