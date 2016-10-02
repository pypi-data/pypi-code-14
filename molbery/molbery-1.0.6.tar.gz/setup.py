# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('molbery/molbery.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "molbery",
    packages = ["molbery"],
    entry_points = {
        "console_scripts": ['molbery = molbery.molbery:main']
      },
    version = version,
    description = "A tool for Molecular biologists to design modified Molecular Beacons which works on Exonuclease III Aided Target Recycling strategy for the detection of nucleic acid signatures.",
    long_description = long_descr,
    author = "Bhagya C T, Manu S",
    author_email = "bhagyathimmappa@gmail.com",
    maintainer = "Manu S",
    maintainer_email = "manuvaivasvata7@gmail.com",
    url = "https://github.com/bhagya-ct/molbery",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
      ],
    keywords=['molecular beacons','EATR',"CEAM","EXOIII","Target recycling"],
    install_requires=[
          'biopython','tabulate','regex','joblib','argparse',
      ],
    include_package_data=True,
    zip_safe=False
    )
