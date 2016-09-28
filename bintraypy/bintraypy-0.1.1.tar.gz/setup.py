from setuptools import setup

dependencies = [
  'requests'
]

setup(
  name='bintraypy',
  version='0.1.1',
  description='Wrapper for (parts of) the Bintray API',
  url='http://github.com/Gohla/bintraypy',
  author='Gabriel Konat',
  author_email='g.d.p.konat@tudelft.nl',
  license='Apache 2.0',
  packages=['bintraypy'],
  install_requires=dependencies,
  test_suite='nose.collector',
  tests_require=['nose>=1.3.7'] + dependencies
)
