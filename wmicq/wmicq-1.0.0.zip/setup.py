import sys
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

if sys.version_info < (3, 4):
    required_packages = ['enum34']
else:
    required_packages = []    


setup(name='wmicq',
      version='1.0.0',
      description='Simple  wrapper for wmic Windows command allowing to query Windows Management Instrumentation (WMI)',
      long_description=readme(),
      url='https://pypi.python.org/pypi/wmicq',
      download_url="https://pypi.python.org/pypi/wmicq",
      author='baseIT',
      author_email='baseit.app+wmicq@gmail.com',
      maintainer='baseIT',
      maintainer_email='baseit.app+wmicq@gmail.com',
      license='MIT',
      packages=['wmicq'],
      install_requires=required_packages,
      include_package_data=True,
      zip_safe=False,
      keywords = "WMI wmic",
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: Microsoft :: Windows',
      ])