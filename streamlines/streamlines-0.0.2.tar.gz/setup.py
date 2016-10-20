from setuptools import setup

setup(
    name="streamlines",
    version="0.0.2",
    packages=["streamlines"],
    license="License :: OSI Approved :: MIT License",
    author="John Bjorn Nelson",
    author_email="jbn@abreka.com",
    description="Tools for working with files as line streams.",
    long_description=open("README.md").read(),
    url="https://github.com/jbn/streamlines",
    setup_requires=['nose>=1.0']
)
