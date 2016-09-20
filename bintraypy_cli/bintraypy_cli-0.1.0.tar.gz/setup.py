from setuptools import setup

dependencies = [
  'bintraypy>=0.1.0', 'plumbum>=1.6.2'
]

setup(
  name='bintraypy_cli',
  version='0.1.0',
  description='Call (parts of) the Bintray API from the command-line',
  url='http://github.com/Gohla/bintraypy_cli',
  author='Gabriel Konat',
  author_email='g.d.p.konat@tudelft.nl',
  license='Apache 2.0',
  packages=['bintraypy_cli'],
  install_requires=dependencies,
  test_suite='nose.collector',
  tests_require=['nose>=1.3.7'] + dependencies,
  entry_points={
    'console_scripts': [
      'bintraypy = bintraypy_cli.main:main'
    ],
  }
)
