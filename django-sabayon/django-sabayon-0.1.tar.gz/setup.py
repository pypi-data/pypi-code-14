from setuptools import setup, find_packages

setup(
    name='django-sabayon',
    version='0.1',
    packages=find_packages(),
    install_requires=['Django>=1.10'],
    author='w0de',
    author_email='harry@sysop.ooo',
    description='Django support for https://github.com/dmathieu/sabayon'
)
