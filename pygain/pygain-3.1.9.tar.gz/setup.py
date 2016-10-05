from setuptools import setup

PACKAGE = "pygain"
NAME = "pygain"
DESCRIPTION = "import module from the sky"
AUTHOR = "zig"
AUTHOR_EMAIL = "remember1637@gmail.com"
URL = "https://github.com/shawhen/pygain"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst", "r").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=["pygain"],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
)
