from setuptools import setup

# Based heavily off forecastiopy by David Ervideira david.dme@gmail.com
# Completely rewritten to improve reability

setup(name='darkskypy',
      version='0.2',
      description='A different python wrapper to access weather data provided by DarkSky.net',
      url='https://github.com/mattbox/DarkSkyPy',
      author='mattbox',
      author_email='mattbox@noreply.github.com',
      license='MIT',
      py_modules=['darksky'],
      install_requires=[
          'requests',
          'attrdict',
      ],
      zip_safe=False)
