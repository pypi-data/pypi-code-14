from setuptools import setup, find_packages

requires = ["fluent-logger == 0.4.4"]

setup(
    name='bufferapp-logger',
    version='0.0.5',
    url='https://github.com/bufferapp/python-logger',
    download_url='https://github.com/bufferapp/python-logger/archive/master.zip',
    author='Steven Cheng',
    author_email='stevenc81@gmail.com',
    description='Python Logger library for Bufferapp.',
    packages=find_packages(exclude=['tests']),
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
)
