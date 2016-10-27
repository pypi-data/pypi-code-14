from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='rainstorm',
    version='0.0.2',
    description='A python ORM with an edge',
    long_description=readme(),
    keywords='database orm',
    license='Apache-2.0',
    url='https://github.com/asfer/rainstorm',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Code Generators',
    ],
    author='Andre Fernandes',
    author_email='andrefernandes6@gmail.com',
    packages=['rainstorm'],
    install_requires=[
        'markdown'
    ],
    include_package_data=True,
    zip_safe=False
)
