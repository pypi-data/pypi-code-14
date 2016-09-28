from distutils.core import setup

setup(
    name='psftp',
    version='0.0.1',
    packages=['psftp'],
    url='https://github.com/bsimpson888/psftp',
    license='GPL',
    author='Marco Bartel',
    author_email='bsimpson888@gmail.com',
    description='a sftp client and server library based on paramiko',
    install_requires=['paramiko']
)
