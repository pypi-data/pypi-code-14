from setuptools import setup, find_packages

long_description = 'Short URLs service for OpenTherapeutics.'
version = __import__('shorturls').__version__

setup(
    name='shorturls',
    url='https://github.com/OpenTherapeutics/shorturls',
    author='Open Therapeutics',
    author_email='mkoistinen@opentherapeutics.org',
    description='Short URLs service for OpenTherapeutics.',
    version=version,
    long_description=long_description,
    platforms=['any'],
    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    package_data={'ot': ['locale/*/*/*.*']},
    requires=[
    ],
    install_requires=[
        'pycrypto>-2.6.1',
        'Django>=1.10,<1.11',
    ]
)
