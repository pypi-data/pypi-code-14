from setuptools import setup

setup(name='amifinder',
    version='0.0.2',
    description='Command line tool to find AMI IDs for a few OS',
    url='https://github.com/mbrannigan/amifinder',
    author='Mike Brannigan',
    license='MIT',
    packages=['amifinder'],
    zip_safe=False,
    install_requires=[
        'click',
        'boto3',
    ],
    entry_points = {
        'console_scripts': ['amifinder=amifinder.cli:main'],
    }
)
