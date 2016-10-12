from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name="rhyme-haiker",
    version="2.0.5",
    description='A rhyming haiku generator.',
    long_description=readme,
    url='https://github.com/shitake/rhyme-haiker',
    author="pochiyuru",
    author_email='pochiyuru@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications'
    ],
    keywords='rhyme haiku',
    packages=find_packages(),
    install_requires=[
        'mecab-python3==0.7'
    ],
    data_files=[],
    entry_points={
        'console_scripts': [
            'haiku=poetry.utils.argparsers:main',
        ],
    },
    test_suite='tests',
)
