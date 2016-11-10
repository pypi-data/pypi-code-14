from distutils.core import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pysodbm',
    version='0.9.13',
    packages=['pysodbm'],
    url='https://github.com/bsimpson888/pysodbm',
    license='GPL',
    author='Marco Bartel',
    author_email='bsimpson888@gmail.com',
    description='A ORM Database layer',
    install_requires=requirements,
    data_files=[('', ['requirements.txt'])]
)
