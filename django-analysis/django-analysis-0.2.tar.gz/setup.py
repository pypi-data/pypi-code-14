import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-analysis',
    version='0.2',
    packages=['analysis'],
    include_package_data=True,
    license='BSD License',
    description='A analysis tool for django app.',
    long_description=README,
    url='https://github.com/Yooke/django-analysis',
    author='Em Lei',
    author_email='live1989@foxmail.com',
)
