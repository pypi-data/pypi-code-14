from setuptools import setup, find_packages


setup(
    name='pixelcms-server',
    version='0.2.1',
    description='PixelCMS server part.',
    url='https://github.com/HurtowniaPixeli/pixelcms-server',
    author='Michał Werner',
    author_email='michal@hurtowniapixeli.pl',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.10,<1.11',
        'django-autoslug>=1.9.3,<2',
        'django-cron>=0.4.6,<1',
        'django-filebrowser>=3.7.2,<4',
        'django-grappelli>=2.8.1,<3',
        'django-polymorphic>=1.0,<2',
        'djangorestframework>=3.4.6,<4',
        'djangorestframework-camel-case>=0.2.0,<1',
        'drfdocs>=0.0.11,<1',
        'Pillow>=3.3.1,<4',
        'psycopg2>=2.6.2,<3',
        'Pygments>=2.1.3,<3',
        'requests>=2.11.1,<3',
        'sqlparse>=0.2.1,<1',
        'Unidecode>=0.4.19,<1'
    ],
    scripts=['cms/bin/pixelcms_bootstrap']
)
