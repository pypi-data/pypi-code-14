from setuptools import setup

requires = [
    'cassandra-driver',
    'paramiko==1.17.0',
    'requests',
    'pyyaml'
]


packages = [
    'tinyblox',
]

setup(name='tinyblox',
      packages=packages,
      version='0.1.9',
      description='Python Automation Framework',
      author='Kiran Vemuri',
      author_email='kkvemuri@uh.edu',
      url='https://github.com/DreamForgeContrive/tinyblox',
      download_url='https://github.com/DreamForgeContrive/tinyblox/tarball/0.1.9',
      keywords=['automation', 'ssh', 'sftp', 'openstack', 'logging', 'cassandra'],
      license='MIT',
      install_requires=requires,
      setup_requires=requires,
      classifiers=[],)
