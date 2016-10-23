#El codigo de este archivo es necesario para empaquetar los archivos python
from distutils.core import setup

setup(
    name="MiPaquete",
    version="1.1",
    packages=["mipaquete",],
    license="MIT",

long_description=open("README.txt").read(),
    )
