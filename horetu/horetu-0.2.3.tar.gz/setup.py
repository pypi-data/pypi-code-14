from distutils.core import setup

packages=[
    'horetu',
    'funmap',
    'triedict',
    'horetu.input', 
    'horetu.output',
    'horetu.render',
]

from setuptools import find_packages
packages = find_packages()

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://src.thomaslevine.com/horetu/',
      packages=packages,
      include_package_data=True,
      install_requires=[
          'Jinja2',
      #   'inflection>=0.3.1', # for singularize
      ],
      extras_require={
          'docs': [
              'sphinxcontrib-autorun>=0.1',
          ],
          'tests': ['pytest>=2.6.4'],
          'dev': ['horetu[docs]', 'horetu[tests]']
      },
      tests_require=[
          'horetu[tests]',
      ],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      version='0.2.3',
      license='AGPL',
      )
