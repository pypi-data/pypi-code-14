from setuptools import setup, find_packages

setup(
	name='QualiCSCLI',
	version='0.8',
	py_modules=['QualiCSCLI'],
	packages=find_packages(),
	install_requires=['requests',],
	author="graboskyc",
	author_email="chris@grabosky.net",
	entry_points='''
		[console_scripts]
		QualiCSCLI=QualiCSCLI:cli
	''',
)
