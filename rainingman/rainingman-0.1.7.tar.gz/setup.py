# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rainingman',
    version='0.1.7',
    description='Raining is a collection of scripts that gather informatio about your packages',
    long_description=long_description,
    url='https://github.com/PET-UnB/pet',
    author='Tiago Assuncao',
    author_email='tiago@sof2u.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Libraries :: Perl Modules',
        'Topic :: Software Development :: Version Control',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='debian packaging development',
    packages=find_packages('rainingman'),
    install_requires=[
    ],
    platforms='any',
    entry_points={
        'console_scripts': [
            'rainingman=rainingman.teste:teste',
        ],
    },
)
