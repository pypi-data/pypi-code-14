#! /usr/bin/env python

import sys

from setuptools import setup , find_packages


setup(name="onyxproject",
      description="Intelligent Dashboard",
      long_description=open("README.rst").read(),
      version='0.2.2',
      packages=find_packages(),
      include_package_data=True,
      url="https://gitlab.com/Aituglo/Onyx",
      maintainer=("Aituglo"),
      maintainer_email="project@onyxlabs.fr",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Build Tools",
          "Topic :: System :: Software Distribution"],
      zip_safe=True,
      entry_points={
          'console_scripts': ['onyxstart=onyx:run']
      },
      install_requires=['pip','Flask==0.10.1','Flask-WTF==0.8.3','Flask-sqlalchemy','requests','beautifulsoup4','Flask-Menu','Flask-Login','SQLAlchemy-migrate','flask_bcrypt','flask-Mail','blinker','wikipedia','markupsafe'],
      options={
          'bdist_wheel': {'universal': True},
      },
      platforms=['any'],
      )
