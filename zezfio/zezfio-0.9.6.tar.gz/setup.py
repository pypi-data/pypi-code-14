from setuptools import setup, Extension

gz2ar = "./zezfio/io/gz2ar"
module = Extension("zezfio.io.gz2ar",
                    libraries = ['z'],
                    sources = ['%s.c'%gz2ar])

setup(
  name = 'zezfio',
  packages = ['zezfio','zezfio/template','zezfio/io','zezfio/lib'],
  scripts = ["zlegacy2json", "zfang", "zserver"],
  version = '0.9.6',
  description = 'The lovely client/server version of Ezfio',
  author = 'Thomas applencourt',
  author_email = 'applencourt@irsamc.ups-tlse.fr',
  url = 'https://github.com/TApplencourt/Zezfio2',
  download_url = 'https://github.com/TApplencourt/Zezfio2/archive/master.zip', 
  keywords = ['programming', 'fortran', 'EZFIO','ZMQ'],
  install_requires=['irpy','pyzmq', 'jinja2', 'docopt'],
  ext_modules = [module])
