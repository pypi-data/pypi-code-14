from setuptools import setup, find_packages

setup(
    name='pyNlple',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.2',
    description='NLP procedures in python brought to you by YouScan.',
    author='Paul Khudan',
    author_email='pk@youscan.io',
    company='YouScan Limited',
    url='https://github.com/YouScan/pyNlple',
    install_requires=['requests>=2.9.1',
                      'pandas>=0.19.0',
                      'gensim>=0.13.3'],

    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='pynlple.tests',

)