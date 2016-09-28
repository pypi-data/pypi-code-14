from setuptools import find_packages, setup
import sys

VERSION = '0.2'

scapy_package = 'scapy-python3' if sys.version_info.major==3 else 'scapy'

setup(name="Bgp",
      version=VERSION,
      description="test tool bgp",
      author="Sudarshana K S",
      author_email='sudarshana.ks@gmail.com',
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
      url="http://github.com/sudks/bgp",
      packages=find_packages(),
      package_data={'bgp': ['vlan1001.cfg']},
      #include_package_data = True,
      install_requires=[scapy_package],
      #download_url='https://github.com/sudks/bgp/tarball/' + VERSION,
      keywords=['tcp','bgp', 'scapy', 'network', 'dissect', 'packets']
      )
