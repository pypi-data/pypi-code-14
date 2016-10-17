from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    print('WARN: README conversion to rst skipped.')
    long_description = open('README.md').read()

setup(
    name='sagaconfig',
    packages=['sagaconfig'],
    package_dir={'sagaconfig': 'src'},
    version='0.0.1',
    description='A config helper',
    long_description=long_description,
    author='Sagacify',
    author_email='dev@sagacify.com',
    url='https://github.com/Sagacify/config-py',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ]
)
