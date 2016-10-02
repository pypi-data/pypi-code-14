from setuptools import setup


def get_long_description():
    import os
    import codecs
    fpath_here = os.path.dirname(__file__)
    fpath_readme = os.path.join(fpath_here, 'README.rst')
    return codecs.open(fpath_readme, 'r', 'utf8').read()

setup(
    name='jira-bulk-loader',
    version='0.3.1',
    packages=['jirabulkloader'],
    author='Alexander Dudko',
    author_email='alex.dudko@gmail.com',
    license='Apache 2.0',
    url='https://github.com/oktopuz/jira-bulk-loader',
    scripts=['bin/jira-bulk-loader.py'],
    description='Create tasks in Jira via RESTful API',
    long_description=get_long_description(),
    install_requires=[
        'jira >= 1.0.7',
        'simplejson >= 3.8.1',
    ],
    tests_require=[
        'pytest',
        'mock',
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
)
