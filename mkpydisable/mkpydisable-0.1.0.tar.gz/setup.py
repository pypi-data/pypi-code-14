import os

from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_dir, "VERSION")) as f:
    VERSION = f.read().rstrip()

setup(
    name="mkpydisable",

    version=VERSION,

    install_requires=[
        "mklibpy>=0.4"
    ],

    packages=find_packages(),

    url="https://github.com/MichaelKim0407/mkpydisable",

    license="MIT",

    author="Michael Kim",

    author_email="jinzheng19930407@sina.com",

    description="Disable things in Python",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",

        "Topic :: Software Development :: Libraries"
    ]
)
