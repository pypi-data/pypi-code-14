try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = ['cityhash']

ENTRY_POINTS = '''
        [console_scripts]
        dedup_hash=dedup_hash.dedup_hash:main
'''

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dedup_hash',
    version='0.1.0',
    packages=['dedup_hash'],
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    entry_points=ENTRY_POINTS,
    keywords='Bioinformatics',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    url='https://github.com/mvdbeek/dedup_hash',
    license='MIT',
    author='Marius van den Beek',
    author_email='m.vandenbeek@gmail.com',
    description='Finds and discards exact duplicate reads in fastq files.'
)
