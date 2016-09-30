from distutils.core import setup

setup(
    name='supermovies',
    version='0.1.1',
    url='http://teachersdunet.com/',
    packages=['supermovies',],
    author='Honore Hounwanou',
    author_email='mercuryseries@gmail.com',
    description=('Sample Python Project for TDN Python Course '
                 'learn how to program in Python.'),
    license='MIT',
    scripts=['supermovies/bin/lambo.py'],
    keywords = ['learn', 'python', 'tdn'],
    long_description=open('README.txt').read(),
)