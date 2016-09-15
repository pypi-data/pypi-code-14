from setuptools import setup

setup(name='azurerm',
      version='0.6.5',
      description='Azure Resource Manager REST wrappers',
      url='http://github.com/gbowerman/azurerm',
      author='sendmarsh',
      author_email='guybo@outlook.com',
      license='MIT',
      packages=['azurerm'],
      install_requires=[
          'adal',
          'requests',
      ],
      zip_safe=False)
