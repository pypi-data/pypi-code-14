from setuptools import setup, find_packages
setup(
    name = "trileans",
    version = "1.5",
    packages = ['trileans'],
    author = "rittbys",
    description = "Trileans are three-valued objects.",
    license = "MIT",
    keywords = "Trileans objects",
    url = "https://github.com/rittbys/Trileans",
    install_requires=[
        "enum",
    ]
)