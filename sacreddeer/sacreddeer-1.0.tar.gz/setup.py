import setuptools


def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(
    name='sacreddeer',
    version='1.0',
    description='Ask your stupid questions and Deer will answer',
    url='http://github.com/pannkotsky/sacreddeer',
    author='Valerii Kovalchuk',
    author_email='kovvalole@gmail.com',
    license='MIT',
    packages=['sacreddeer'],
    install_requires=[
        'slackclient',
    ],
    scripts=['cmd/deer'],
    zip_safe=False
)
