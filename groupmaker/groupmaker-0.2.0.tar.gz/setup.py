"""Package definition for groupmaker."""
from setuptools import setup


setup(
    name='groupmaker',
    version='0.2.0',
    description='Command line tool for making classroom groups.',
    url='https://github.com/selassid/groupmaker',
    author='David Selassie',
    author_email='selassid@gmail.com',
    license='BSD',
    packages=['groupmaker'],
    scripts=[
        'bin/groupmaker',
    ],
    install_requires=[
        'tabulate',
    ],
    zip_safe=True,
)
