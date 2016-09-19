from setuptools import setup


with open('README.rst', 'r') as f:
    long_description = f.read().split('\n\n-----\n\n', 1)[1].lstrip()

setup(
    name='deasciiify',
    version='0.0.1',
    description='Translate ASCII text into readable non-ASCII text',
    long_description=long_description,
    url='https://github.com/jnrbsn/deasciiify',
    author='Jonathan Robson',
    author_email='jnrbsn@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    py_modules=['deasciiify'],
)
