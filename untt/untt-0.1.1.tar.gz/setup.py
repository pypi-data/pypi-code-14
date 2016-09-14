from os import path
import codecs

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with codecs.open(path.join(here, 'requirements.txt'),
                 encoding='utf-8') as reqs:
    requirements = reqs.read()

setup(
    name='untt',
    version='0.1.1',

    description='Right, it\'s uEntity.',
    long_description="""
    """,

    url='http://untt.n9co.de',

    author='Bagrat Aznauryan',
    author_email='bagrat@aznauryan.org',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='model orm entity untt',

    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=requirements,
)
