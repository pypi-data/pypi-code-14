from setuptools import find_packages, setup

setup(
    name='cairy',
    version='0.1',
    description='lightweight lib that allows easy transformation of data from one json mapping to another',
    url='https://github.com/rutherford/cairy',
    author='Matt Rutherford',
    author_email='rutherford@clientsideweb.net',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='json template mapping transformation',
    packages=find_packages(exclude=[]),
    install_requires=[]
)