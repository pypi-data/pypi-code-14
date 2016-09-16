"""Laminate - Create beatifull yet simple html and pdf documents
from markdown
"""
from setuptools import setup

setup(name='laminate',
      version='0.5',
      url='https://github.com/ohenrik/laminate',
      description='Tool for creating styled html and pdf from markup',
      long_description=__doc__,
      author='Ole Henrik Skogstrøm',
      author_email='laminate@amplify.no',
      packages=['laminate'],
      include_package_data=True,
      install_requires=[
          'docopt>=0.6.2',
          'Jinja2>=2.8',
          'Markdown>=2.6.6',
          'markdown-include>=0.5.1',
          'laminate_default>=0.2'
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha'
      ]
     )

__author__ = 'Ole Henrik Skogstrøm'
