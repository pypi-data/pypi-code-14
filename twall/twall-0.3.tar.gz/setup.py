from setuptools import setup, find_packages

setup(
    name='twall',
    version='0.3',
    description='Twitter Wall project for MI-PYT by Daniel Maly',
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
    install_requires=['flask', 'click>=6', 'requests']
)
