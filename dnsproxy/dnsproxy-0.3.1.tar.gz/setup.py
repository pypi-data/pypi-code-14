from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    readme = f.read()


setup(
    name='dnsproxy',
    version='0.3.1',
    packages=['dnsproxy'],
    install_requires=[
        'dnslib',
        'falcon',
        'gevent',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'dnsproxy=dnsproxy.client:main',
            'dnsproxy_server=dnsproxy.server:main',
        ]
    },
    description='Secure DNS proxy',
    long_description=readme,
    author='Harry Liang',
    author_email='blurrcat@gmail.com',
    url='https://github.com/blurrcat/dnsproxy',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['dns', 'proxy'],
)
