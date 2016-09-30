from distutils.core import setup

setup(
    name='supermovies',
    version='0.1.7',
    url='http://teachersdunet.com/',
    packages=['supermovies',],
    author='Honore Hounwanou',
    author_email='mercuryseries@gmail.com',
    description=('Sample Python Project for TDN Python Course '
                 'learn how to program in Python.'),
    license='MIT',
    scripts=['supermovies/bin/lambo.py', 'supermovies/bin/lambo', 'supermovies/bin/movies.csv'],
    keywords = ['learn', 'python', 'tdn'],
    long_description=open('README.txt').read(),
)