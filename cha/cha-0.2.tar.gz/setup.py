from setuptools import setup


setup(
    name="cha",
    version="0.2",
    license='MIT',
    url='https://github.com/ubear/cha/',
    author="chyoo",
    keywords='Sample cli tool to translate English to Chinese',
    author_email="chyoo1991@gmail.com",
    packages=['cc'],
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    install_requires=[
        'requests>=2.2.1',
        'BeautifulSoup>=3.2.1',
        'sqlalchemy>=1.0.14',
    ],

    classifiers=[

    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'c=cc.c:make_cli',
        ],
    },
)
