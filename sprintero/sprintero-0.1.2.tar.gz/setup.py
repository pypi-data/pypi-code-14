import os

from setuptools import find_packages, setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='sprintero',
    version='0.1.2',
    description='Sprint name generator',
    long_description=README,
    author='Sebastian Opalczynski',
    author_email='opalczynski@gmail.com',
    url='https://github.com/opalczynski/sprintero',
    packages=find_packages(),
    package_data={'sprintero.names_collection.marvel': ['*.data']},
    license='MIT',
    install_requires=['click>=6.6'],
    entry_points="""
        [console_scripts]
        sprintero=sprintero.main:main
    """
)
