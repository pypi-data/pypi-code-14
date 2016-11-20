from setuptools import setup #enables develop

setup(name='robotapi',
      version='1.0',
      description='Python API for mobile robot control',
      author='Parin Chheda, Saurav Shandilya',
      author_email='sauravs.iitb@gmail.com',
      license='BSD',
      scripts=[],
      url='https://github.com/sauravshandilya/SDES-2016-Project2',
      packages=['source'],
      install_requires=[
        "mock",
        "pyserial",
        "nose",
      ],
)