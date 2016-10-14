import os

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') if os.path.exists('README.rst') else \
        open('README.md', encoding='utf-8') as fileobj:
    long_description = fileobj.read()

setup(
    name='bio-mimo',
    version='1.1.3',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/childsish/bio-mimo',
    license='LICENSE',
    description='A MiMo library for biological data',
    long_description=long_description,
    install_requires=['lhc-python', 'mimo'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics']
)
