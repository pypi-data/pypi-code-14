from setuptools import setup

setup(
    name='cricketscore',  # This is the name of your PyPI-package.
    version='0.5',  # Update the version number for new releases
    scripts=['bin/cricketscore.py'],
    description='A simple tool to crawl latest cricket score and show notification for the same',
    author='Rajat Bhardwaj',
    author_email='bhardwaj.rajat18@gmail.com'
)
