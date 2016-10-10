# http://bugs.python.org/issue15881#msg170215
from setuptools import setup, find_packages

from os import listdir

setup(
    name="stacks_summary",
    version='1.1',
    description="Stacks reports generator",
    author="Maria Bernard",
    author_email="maria.bernard@inra.fr",
    url="https://github.com/mariabernard/galaxy_wrappers",
    install_requires=['numpy'],
    packages=find_packages(),
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    scripts=['stacks_summary.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ],
    include_package_data = True,
)
