from setuptools import setup

setup(name='python_gyg',
      version='0.1',
      description='Python library for GetYourGuide API',
      url='http://github.com//fukac99/python_gyg.git',
      long_description="""
      This is a pure Python library, handling all the connections to the GetYourGuide APIv1. It
supports searches for locations and tours by different parameters. Fro further information
on GetYourGuide API and for obtaining the api key checkout http://getyourguide.com
""",
      keywords=['getyourguide', 'travel', 'api', 'tours'],
      classifiers=[
	'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
],
      author='Lukas Toma',
      install_requires=["requests", "datetime"],
      author_email='toma.lukas@gmail.com',
      license='MIT',
      packages=['python_gyg'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose', "datetime"])
