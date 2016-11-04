from distutils.core import setup

setup(
    name='pysodbm',
    version='0.9.11',
    packages=['pysodbm'],
    url='https://github.com/bsimpson888/pysodbm',
    license='GPL',
    author='Marco Bartel',
    author_email='bsimpson888@gmail.com',
    description='A ORM Database layer',
    install_requires=['pymysql', 'estoolbox', 'xyaml', 'future']
)
