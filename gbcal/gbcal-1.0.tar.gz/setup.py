# from distutils.core import setup
from setuptools import setup

setup(
    name="gbcal",
    version='1.0',
    description="cli tool to manage google birthday calendar",
    author="Daniel Kraic",
    author_email="danielkraic@gmail.com",
    url="https://github.com/danielkraic/gbcal",
    packages=["gbcal"],
    license='MIT',
    install_requires=[
          'google-api-python-client',
      ],
    entry_points = {
        'console_scripts':
            ['gbcal = gbcal.main:main'],
    },
)