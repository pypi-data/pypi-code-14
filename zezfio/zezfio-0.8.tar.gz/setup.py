from setuptools import setup, Extension

module = Extension('gz2ar',
                    libraries = ['z'],
                    sources = ['./zezfio/io/gz2ar.c'])

setup(
  name = 'zezfio',
  packages = ['zezfio'],
  scripts = ["zlegacy2json.py", "zfang.py", "zserver.py"],
  version = '0.8',
  description = 'The lovely client/server version of Ezfio',
  author = 'Thomas applencourt',
  author_email = 'applencourt@irsamc.ups-tlse.fr',
  url = 'https://github.com/TApplencourt/Zezfio2',
  download_url = 'https://github.com/TApplencourt/Zezfio2/archive/master.zip', 
  keywords = ['programming', 'fortran', 'EZFIO','ZMQ'],
  install_requires=['irpy','pyzmq', 'jinja2'],
  ext_modules = [module])