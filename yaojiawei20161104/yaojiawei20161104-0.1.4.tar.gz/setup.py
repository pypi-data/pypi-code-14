from setuptools import setup, find_packages

setup(name='yaojiawei20161104',
    version='0.1.4',

    description='WSGI HTTP Server for UNIX',
    author='Benoit Chesneau',
    author_email='benoitc@e-engura.com',
    license='MIT',
    url='http://gunicorn.org',
    zip_safe=False,
   	packages=find_packages(exclude=['examples', 'tests']),
    #include_package_data=True,
    # packages=['yaojiawei20161104','yaojiawei20161104/zz','yaojiawei20161104/skels/yaojiawei'],
    entry_points="""
    [console_scripts]
    yaojiawei=yaojiawei20161104.skels.yaojiawei:hehe
    """)
