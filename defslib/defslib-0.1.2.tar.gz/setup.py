from distutils.core import setup
setup(
  name = 'defslib',
  packages = ['defslib'],
  version = '0.1.2',
  description = 'Baserock definitions parser',
  author = 'Daniel Firth',
  author_email = 'locallycompact@gmail.com',
  url = 'https://gitlab.com/baserock/spec',
  keywords = [],
  classifiers = [],
  package_data={'defslib': ['spec/schemas/*.json-schema', 'spec/schemas/*.json-schema']}
)
