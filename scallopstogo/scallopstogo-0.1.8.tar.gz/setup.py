from setuptools import setup#, find_packages

DESCRIPTION = (
    "Package for integration of Google Calendar in BI"
)

#with open('README.md') as f:
#    readme = f.read()

setup(
    name="scallopstogo",
    version="0.1.8",
    author="Andrew Lee",
    author_email="andrewlee@indeed.com",
    license="Reserved",
    description=DESCRIPTION,
    packages=['scallopstogo']
)