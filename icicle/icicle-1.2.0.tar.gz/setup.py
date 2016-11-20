from setuptools import setup

setup(
    name='icicle',
    version='1.2.0',
    description='Python FrozenDict',
    url='https://github.com/pcattori/icicle',
    author='Pedro Cattori',
    author_email='pcattori@gmail.com',
    license='MIT',
    packages=['icicle'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='frozendict immutable hash mapping'
)
