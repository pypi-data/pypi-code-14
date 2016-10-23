from setuptools import setup

setup(
    name='DBcm',
    version='1.7.0',
    description='The Head First Python 2e Database Context Manager',
    long_description="""
    The Head First Python Database Context Manager.

    Devised, coded, and built during Chapters 7, 8, and 9 of the 2nd edition
    of Head First Python (by O'Reilly Media).  Used and extended with support
    for custom exceptions in Chapter 11.

    Released into the wild at the suggestion of one of Paul's ex-students (thanks @csl_).

    If you really need to do stuff like this, use SQLAlchemy (and/or Dataset) instead.

    Python 3 only (due to type hints and new syntax).  Should be easy enough to backport
    if you need to.  Also: from v1.7.x this code takes advantage of raise's "from" syntax.
    """,
    author='Paul Barry',
    author_email='paul.james.barry@gmail.com',
    url='http://www.headfirstlabs.com',
    py_modules=['DBcm'],
    dependency_links=['http://dev.mysql.com/downloads/connector/python/'],
    license='MIT',
    install_requires=['mysql-connector-python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    
)
