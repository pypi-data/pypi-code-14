import re
from setuptools import setup, find_packages

# Parse the version from the __init__.py file
version = ''
with open('tfstate/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name="tfstate",
    version=version,
    license="MIT",
    author="Reuven V. Gonzales",
    url="https://github.com/virtru/tfstate",
    author_email="reuven@virtru.com",
    description="Turns terraform output into json from the CLI",
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='*nix',
    install_requires=[
        "click==5.1",
    ],
    entry_points={
        'console_scripts': [
            'tfstate = tfstate.cli:cli',
        ],
    },
    classifiers = [],
)
