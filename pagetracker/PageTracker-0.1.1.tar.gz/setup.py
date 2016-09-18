from distutils.core import setup

setup(
    name='PageTracker',
    version='0.1.1',
    author='rakesh sukumar',
    author_email='rsukuma2@ncsu.edu',
    packages=['PageTracker'],
    url='http://pypi.python.org/pypi/PageTracker/',
    license='LICENSE.txt',
    description='Tracks pages and sends out email alerts when the page changes',
    long_description=open('README.txt').read(),
    install_requires=[
       "beautifulsoup4>=4.5.1",
       "bs4>=0.0.1",
       "requests>=2.11.1",
       "simplejson>=3.8.2"
    ],
)