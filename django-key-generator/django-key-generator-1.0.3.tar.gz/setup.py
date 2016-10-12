from setuptools import find_packages, setup

setup(
	name='django-key-generator',
	version='1.0.3',
	description='A django-admin command to generate a secret key',
	url='https://github.com/TrianglePlusPlus/django-key-generator',
	author='Triangle++',
	author_email='justice.suh@gmail.com',
	license='MIT',
	packages=find_packages(),
	install_requires=['django']
	)