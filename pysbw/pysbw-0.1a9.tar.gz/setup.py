from setuptools import setup, find_packages

__version__ = None
exec(open('pysbw/_version.py').read())  # load the actual __version__

README = open('README.rst', "r").read()

setup(
    name='pysbw',
    version=__version__,
    maintainer='Arman Noroozian',
    maintainer_email='arman.noroozian.developer@gmail.com',
    url='https://bitbucket.org/arman_noroozian/pysbw',
    description='Python API Implementation for Accessing Stopbadware Data Feed',
    # long_description_markdown_filename='README.md',
    long_description=README,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='stopbadware api download',
    # py_modules=['__init__', '_version'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    tests_require=['nose', 'coverage'],
    zip_safe=False,
    test_suite='nose.collector',
    # packages=find_packages(exclude=['tests', 'tests.*']),
    # setup_requires=[],
    install_requires=['requests', 'pypandoc', 'setuptools-markdown'],
    # data_files=[],
    # scripts=[],
    # **extra_kwargs
)


