from setuptools import setup

setup(
    name='jsonic',
    version='1.0.0',
    description='Utilities for handling streams of JSON objects',
    url='https://github.com/pcattori/jsonic',
    author='Pedro Cattori',
    author_email='pcattori@gmail.com',
    license='MIT',
    packages=['jsonic'],
    install_requires=[
        'six>=1.10.0'
    ],
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ]
)
