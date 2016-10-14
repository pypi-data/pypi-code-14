from setuptools import setup, find_packages
from codecs import open

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

APP_NAME = 'inject-emoji'
VERSION = '1.0.0'

REQUIRES = []

setup(
    name=APP_NAME,
    version=VERSION,
    description='Emoji notation expansion.',
    author='Clay Loveless',
    author_email='clay@loveless.net',
    url='https://github.com/claylo/inject-emoji',
    license=license,
    keywords=['emoji','github','markdown'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=REQUIRES,
    packages=find_packages(exclude=('tests', 'emojis', 'media')),
    include_package_data=True,
    long_description=readme,
    extras_require={
        'test': ['coverage', 'coveralls', 'pytest', 'pytest-instafail'],
        'develop': [
            'coverage',
            'coveralls[yaml]',
            'pytest',
            'pytest-instafail'
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'inject-emoji = inject_emoji.cli:main'
        ]
    }
)
