from setuptools import setup, find_packages

setup(name = "peekSSD",
    version = "1.0.3",
    description = "An APP to peek SSD Device Performance",
    author = "Shannon FAE Team",
    author_email = "pingyu@shannon-data.com",
    url = "",
    packages = ['peekSSD'],
    include_package_data = True,
    package_data = {
		'peekSSD' : ["sh/*"],
		'peekSSD' : ["gnuplot/*"],
		 },
    entry_points = {
        'console_scripts': [
            'show_stable = peekSSD.show_stable:main',
	    'show_spec = peekSSD.show_spec:main'
        ]
    },
    long_description = """An APP to peek SSD Device Performance developped by Shannon FAE Team""", 
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]     
) 
