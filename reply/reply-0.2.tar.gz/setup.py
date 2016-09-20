from distutils.core import setup

setup(
    name='reply',
    version='0.2',
    url='https://github.com/JavierLuna/reply',
    author='Javier Luna Molina',
    author_email='javierlunamolina@gmail.com',
    description='Test your front-end calls easily!',
    long_description='Make a simple server to test your front-end or mobile app calls',
    packages=['reply'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server'
        ],
)