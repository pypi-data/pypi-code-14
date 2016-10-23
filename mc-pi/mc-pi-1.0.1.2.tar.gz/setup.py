import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mc-pi",
    version = "1.0.1.2",
    author = "Martin O'Hanlon",
    author_email="sr.tama@outlook.com",
    description = ("Refer to http://www.stuffaboutcode.com"),
    keywords = "raspberry pi minecraft python tutorial",
    url = "https://github.com/MrMenezes/mcpi",
    packages=['mcpi'],
    long_description=read('README.md'),
)
