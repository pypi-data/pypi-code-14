from setuptools import setup

setup(
   name='switchDiscovery',
   version='1.2.0.dev1',
   description='CISCO Switch Devices Discovery tool',
   author='Aniket Gole',
   author_email='roshan3133@gmail.com',
   license='MIT',
   classifiers=['Development Status :: 3 - Alpha', 
     'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4'	
],	
   keywords= ['Cisco Switch information Discovery'],
   packages=['switchDiscovery'], 
   install_requires=['commands', 'paramiko', 'netaddr', 'getpass', 'sys', 'argparse', 'logging'], #external packages as dependencies
   scripts=[],
   include_package_data=True,
   zip_safe=False
)
