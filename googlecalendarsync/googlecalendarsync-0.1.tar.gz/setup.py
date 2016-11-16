from setuptools import setup

setup(name='googlecalendarsync',
      version='0.1',
      description='Module to sync events from your Google calendar',
      url='https://bitbucket.org/diamino/googlecalendarsync',
      author='Diamino',
      author_email='code@diamino.nl',
      license='MIT',
      packages=['googlecalendarsync'],
      install_requires=[
          'oauth2client',
          'google-api-python-client',
      ],
      zip_safe=False)
