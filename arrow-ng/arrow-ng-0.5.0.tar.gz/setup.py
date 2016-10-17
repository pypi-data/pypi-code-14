try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='arrow-ng',
    version='0.5.0',
    description='Better dates and times for Python',
    url='https://github.com/ifanrx/arrow',
    author='ifanr',
    author_email='ifanrx@ifanr.com',
    license='Apache 2.0',
    packages=['arrow'],
    zip_safe=False,
    install_requires=[
        'python-dateutil'
    ],
    test_suite="tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

