from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from codedeploy_generator import __version__

# here = path.abspath(path.dirname(__file__))
#
# # Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='codedeploy_generator',
    version = __version__,

    description='generate deployment scripts for code_deploy',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/bjtox/python_module_test.git',

    # Author details
    author='Antonio Bitonti',
    author_email='antonio.bitonti@gmail.com',
    packages=['codedeploy_generator'],
    # package_dir={'commands': 'codedeploy_generator/commands'},
    package_data={
        'codedeploy_generator': ['./extra/*.*','./commands/*.*'],
    },

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='aws code_deploy deployments',
    install_requires=['docopt','Jinja2'],




    entry_points={
        'console_scripts': [
            'cdgen = codedeploy_generator.cli:main',
        ],
    },
)
