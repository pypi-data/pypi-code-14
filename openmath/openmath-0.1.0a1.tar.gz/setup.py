from setuptools import setup, find_packages

setup(
    name='openmath',
    version='0.1.0a1',
    description='Object implementation of the OpenMath standard',
    url='https://github.com/OpenMath/py-openmath',
    author='Luca De Feo',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='openmath',
    packages=find_packages(),
)
