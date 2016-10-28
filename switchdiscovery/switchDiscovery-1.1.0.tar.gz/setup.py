from setuptools import setup

setup(
   name='switchDiscovery',
   version='1.1.0',
   description='Switch Devices Discovery tool',
   author='Aniket Gole',
   author_email='roshan3133@gmail.com',
   license='MIT',
   packages=['switchDiscovery'],  #same as name
   install_requires=['commands', 'paramiko', 'netaddr', 'getpass', 'sys', 'socket', 'argparse', 'logging'], #external packages as dependencies
   scripts=[],
   include_package_data=True,
   zip_safe=False
)
