from setuptools import setup, find_packages

setup(
    name='pyems',
    version='0.1.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/tomi77/pyems',
    license='MIT',
    author='Tomasz Jakub Rup',
    author_email='tomasz.rup@gmail.com',
    description='Python EMS API wrapper',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)
