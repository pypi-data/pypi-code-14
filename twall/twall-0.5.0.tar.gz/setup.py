from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='twall',
    version='0.5.0',
    description='Twitter Wall project for MI-PYT by Daniel Maly',
    long_description=long_description,
    author='Daniel Malý',
    author_email='maly.dan@gmail.com',
    keywords='twitter,search,wall',
    license='MIT',
    url='https://github.com/DanielMaly/twall',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'twall = twall.twall:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Framework :: Flask',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=['flask', 'click>=6', 'requests'],
    setup_requires=['pytest-runner>=2.9'],
    tests_require=['pytest==2.9.2', 'betamax>=0.8.0', 'betamax-serializers>=0.2.0']
)
