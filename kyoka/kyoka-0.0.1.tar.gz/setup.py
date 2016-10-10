import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "kyoka",
    version = "0.0.1",
    author = "ishikota",
    author_email = "ishikota086@gmail.com",
    description = ("Simple Reinforcement Learning Library"),
    license = "MIT",
    keywords = "reinforcement learning RL",
    url = "https://github.com/ishikota/kyoka",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
    ],
)
