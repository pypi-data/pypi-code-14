from setuptools import setup, find_packages

setup(
      install_requires=['distribute', 'Adafruit_MotorHAT>=1.3.0','nxt-python==2.2.2', 'PyTweening==1.0.3'],
      name = 'drivar',
      description = 'Hardware abstraction layer for Raspbuggy',
      author = 'Brice Copy',
      author_email = 'brice.copy@gmail.com',
      url = 'https://github.com/cmcrobotics/raspbuggy',
      keywords = ['raspbuggy'],
      version = '0.2.5',
      packages =  find_packages('.')
)
