# dataRX : A simple extension used to view, clean, and process your data files
# Author : Rashad Alston <ralston@yahoo-inc.com>
# Python : 3.5.1
#
# License: BSD 3 Clause

from setuptools import setup, find_packages

setup(
	name="dataRX",
	version="2.0",
	description="Extension used to import, read, and give preliminary descriptive statistics of data files.",
	url="https://github.com/ralston3/dataRX/",
	author="Rashad Alston",
	author_email="ralston@yahoo-inc.com",
	packages=find_packages(),
	package_data={"":["LICENSE.txt", "README.md", "requirements.txt"]},
	include_package_data=True,
	platforms="any",
	license="BDS 3 Clause",
	install_requires=[
		"pandas",
		"numpy",
		"scipy"
		],
	zip_safe=False,
	long_description=""" A Python extension for preliminary descriptive stat analysis of a data set.
	
			Contact
			-------
			If you have any questions or comments about dataRX, please feel free to contact me via
			email: rashadaalston@gmail.com. 
			This project is hosted at: https://github.com/ralston3/dataRX
			The documentation can be found at: https://github.com/ralston3/dataRX
	"""
	)