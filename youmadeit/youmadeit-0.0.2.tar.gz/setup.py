from setuptools import setup

setup(name='youmadeit',
      version='0.0.2',
      description='Connection to YouMadeIt service',
      url='http://www.youmadeit.fr',
      author='Enersy',
      author_email='enersy@enersy.fr',
      license='MIT',
      classifiers=[
		    # How mature is this project? Common values are
		    #   3 - Alpha
		    #   4 - Beta
		    #   5 - Production/Stable
		    'Development Status :: 3 - Alpha',

		    # Indicate who your project is intended for
		    'Intended Audience :: Developers',
		    'Topic :: Software Development :: Libraries',

		    # Pick your license as you wish (should match "license" above)
		     'License :: OSI Approved :: MIT License',

		    # Specify the Python versions you support here. In particular, ensure
		    # that you indicate whether you support Python 2, Python 3 or both.
		    'Programming Language :: Python :: 2',
		    'Programming Language :: Python :: 2.6',
		    'Programming Language :: Python :: 2.7',
		    'Programming Language :: Python :: 3',
		    'Programming Language :: Python :: 3.2',
		    'Programming Language :: Python :: 3.3',
		    'Programming Language :: Python :: 3.4',
	  ],
      packages=['youmadeit'],
      install_requires=['paho-mqtt', 'requests', 'simplejson'],
      zip_safe=False)