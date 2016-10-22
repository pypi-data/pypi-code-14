import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='sw_billing',
    version='0.0.1',
    description='Soft-Way billing',
    long_description=README,
    author='nick1994209',
    author_email='nick1994209@gmail.com',
    url='https://gitlab.soft-way.biz/soft-way/billing',
    license='MIT',
    packages=find_packages(exclude='example'),
    include_package_data=True,
    install_requires=[
        # 'sw-python-utils=0.0.13'
    ]
)
