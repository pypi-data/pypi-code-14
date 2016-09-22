from setuptools import setup, find_packages

setup(
    name='vrmapi',
    packages=find_packages(),
    version='0.1.3',
    description='Victron python api',
    install_requires=['requests'],
)
