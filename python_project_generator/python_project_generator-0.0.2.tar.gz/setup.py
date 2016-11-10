from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name="python_project_generator",
    version='0.0.2',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    description='generate a python project',
    long_description=readme,
    author="slumber1122",
    author_email="slumber1122@gmail.com",
    url="https://github.com/slumber1122/python_project_generator",
    license=license,
    entry_points={'console_scripts': [
        'pygen = python_project_generator.generator:main',
    ]},
    packages=find_packages(),
    keywords='structure of python project',
    include_package_data=True,
    zip_safe=False
)
