from setuptools import setup

setup(name='vaultcacli',
      version='0.1',
      description='Create certificates in Vault using a CLI',
      url='http://github.com/larsla/vaultcacli',
      author='Lars Larsson',
      author_email='lars.la@gmail.com',
      license='MIT',
      scripts=['bin/vaultcacli'],
      install_requires=[
          'requests'
      ],
      zip_safe=False)
