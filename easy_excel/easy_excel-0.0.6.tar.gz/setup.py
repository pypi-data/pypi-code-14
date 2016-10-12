import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='easy_excel',
    version='0.0.6',
    description='Python create excel',
    long_description=README,
    author='nick1994209',
    author_email='nick1994209@gmail.com',
    url='https://github.com/Nick1994209/python_easy_excel/',
    license='MIT',
    packages=['easy_excel'],
    # packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'xlwt>=1.0.0',
    ]
)