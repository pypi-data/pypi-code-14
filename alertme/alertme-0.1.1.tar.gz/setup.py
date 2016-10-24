
from distutils.core import setup

setup(
	name='alertme',
	description='Python command line tool that sends email when your script finishes running or has an error',
	version='0.1.1',
	url='http://github.com/ChandranshuRao14/AlertMe/',
	packages=['alertme'],
	scripts=['bin/alertme'],
	author='Chandranshu Rao',
	author_email='chandranshu.rao@gmail.com',
	license='MIT',
	long_description=open('README.txt').read(),
	keywords='alert alertme'
)
