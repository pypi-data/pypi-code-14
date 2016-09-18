from setuptools import setup, find_packages

setup(
    name='bufferapp-logger',
    version='0.0.4',
    url='https://github.com/bufferapp/python-logger',
    download_url='https://github.com/bufferapp/python-logger/archive/master.zip',
    author='Steven Cheng',
    author_email='stevenc81@gmail.com',
    description='Python Logger library for Bufferapp.',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
)
