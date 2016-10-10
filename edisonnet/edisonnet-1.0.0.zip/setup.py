import subprocess
from setuptools import setup

subprocess.call("python install.py", shell=True)

setup(name='edisonnet', version='1.0.0', py_modules = ['install'], packages=['edisonnet'],  install_requires=[
              'Pynetinfo==0.1.9',
                    ],)
