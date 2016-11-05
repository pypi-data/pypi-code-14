from distutils.core import setup

setup(
    name='NetbeansConverter',
    version='1.0',
    packages=[''],
    url='',
    license='MIT',
    author='qinusty',
    author_email='jos67@aber.ac.uk',
    description='Creates necessary config files for a C project to be a netbeans project.',
    scripts=["netbeansconvert.py", "nbconvert"],
    data_files=[("etc", ["configurations.xml", "Makefile", "project.xml"])]
)
