"""
snitch2
-------------
BFS web crawler for searching a domain for specific external links.
"""


from setuptools import setup


setup(
    name='snitch2',
    version='0.2.3',
    url='https://github.com/joelcolucci/snitch2',
    license='MIT',
    author='Joel Colucci',
    author_email='joelcolucci@gmail.com',
    description='Web crawler for searching a domain for specific external links',
    long_description=__doc__,
    packages=['snitch2'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'bs4',
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)