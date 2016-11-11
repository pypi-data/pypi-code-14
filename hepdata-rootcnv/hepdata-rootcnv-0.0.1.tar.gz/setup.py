from setuptools import setup,find_packages

setup(
  name = 'hepdata-rootcnv',
  version = '0.0.1',
  packages = find_packages(),
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  description = 'flexible conversion form ROOT to HepData YAML',
  install_requires = [
    'click'
  ],
  entry_points = {
      'console_scripts': [
        'hepdata-rootcnv = hepdatarootcnv.cli:converter',
      ]
    },
)