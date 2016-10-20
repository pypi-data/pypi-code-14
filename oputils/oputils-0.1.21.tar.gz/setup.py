from distutils.core import setup

setup(
    # Application name:
    name="oputils",

    # Version number (initial):
    version="0.1.21",

    # Application author details:
    author="James Raby",
    author_email="james.raby@lonelyplanet.com",

    # Packages
    packages=["oputils"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/oputils_v0121/",

    #
    # license="LICENSE.txt",
    description="Open planet python utilities",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
    ]
)
