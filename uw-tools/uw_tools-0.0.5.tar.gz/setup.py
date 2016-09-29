from setuptools import setup

long_description = '''A collection of Python scripts that have proven useful and have been reused.

As the files are moved from their original location into this project, we are trying to make sure they are compatible
with both Python 2.7 and 3.5.'''

setup(
    name="uw_tools",
    version="0.0.5",
    author="unfoldingWord",
    author_email="phillip_hopper@wycliffeassociates.org",
    description="A collection of useful scripts",
    license="MIT",
    keywords="unfoldingWord python tools",
    url="https://github.org/unfoldingWord-dev/uw_tools",
    packages=['general_tools', 'uw'],
    long_description=long_description,
    classifiers=[],
    requires=['pygithub', ]
)
