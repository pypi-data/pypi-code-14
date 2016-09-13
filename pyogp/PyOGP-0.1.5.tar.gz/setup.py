from distutils.core import setup
import pypandoc

long_description = pypandoc.convert('README.md', 'rst')

setup(
    name="PyOGP",

    version="0.1.5",

    author="holdonnn",
    author_email="rururu0729@gmail.com",

    # Packages
    packages=["pyogp"],

    # Details
    url="https://github.com/holdonnn/PyOGP/",

    license="LICENSE.txt",
    description="Python Crawler based on Open-Graph Protocol",

    long_description=open("README.rst").read(),

    # Dependent packages (distributions)
)
