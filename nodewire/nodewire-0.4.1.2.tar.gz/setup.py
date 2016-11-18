from setuptools import setup
# https://python-packaging.readthedocs.io/en/latest/minimal.html

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='nodewire',
      version='0.4.1.2',
      description='NodeWire Gateway',
      long_description=readme(),
      url='http://www.nodewire.org',
      author='Ahmad Sadiq',
      author_email='sadiq.a.ahmad@gmail.com',
      license='BSD',
      packages=['nodewire'],
      scripts=['bin/nodewiregw.py', 'bin/nodewireRe.py'],
      install_requires=[
            'paho-mqtt',
            'configparser',
            'netifaces',
            'pyserial',
            'requests'
      ],
      zip_safe=False)
