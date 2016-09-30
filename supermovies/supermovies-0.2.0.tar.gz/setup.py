from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='supermovies',
    version='0.2.0',
    url='http://teachersdunet.com/',
    packages=['supermovies'],
    author='Honore Hounwanou',
    author_email='mercuryseries@gmail.com',
    description=('Sample Python Project for TDN Python Course '
                 'learn how to program in Python.'),
    license='MIT',
    scripts=['bin/netflix.py', 'bin/netflix', 'bin/movies.csv'],
    keywords = ['learn', 'python', 'tdn'],
    long_description=readme()
)