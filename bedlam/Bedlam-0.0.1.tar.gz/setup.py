from setuptools import find_packages, setup


# python setup.py sdist upload


long_desc = '''\

'''


if __name__ == '__main__':
    setup(
        packages=find_packages(),
        name='Bedlam',
        version='0.0.1',
        author='Christopher Sira',
        author_email='cbsira@gmail.com',
        license='BSD',
        url='https://github.com/csira/bedlam',
        description='',
        long_description=long_desc,
        install_requires=[
            'gunicorn',
            'ujson',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: Freely Distributable',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
