import sys
import os
import subprocess
from distutils.core import setup
from distutils.command.install import install

if sys.version_info[0] < 3:
  sys.stderr.write('Only Python 3 supported\n')
  sys.exit(1)

class install_native_app(install):

  def run(self):
    super().run()
    print("Installing native host application ")
    script = self.distribution.get_command_obj('install_scripts').get_outputs()[0]
    subprocess.call([script, "install"])

setup(
  name="chrome-pass",
  version="0.1.2",
  description="Chrome Native application for pass - the standard Unix password manager",
  url="https://github.com/hsanson/chrome-pass",
  author="Horacio Sanson",
  author_email="e@e.com",
  license="MIT",
  install_requires=['python-gnupg'],
  scripts=["nativePass"],
  cmdclass={ 'install': install_native_app }
  )
