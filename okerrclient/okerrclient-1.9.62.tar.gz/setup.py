from setuptools import setup

setup(name='okerrclient',
    version='1.9.62',
    description='client for okerr cloud monitoring system',
    url='http://okerr.com/',
    author='Yaroslav Polyakov',
    author_email='xenon@sysattack.com',
    license='MIT',
    packages=['okerrclient'],
    scripts=['scripts/okerrclient'],
    data_files = [
        ('okerrclient',['data/oc', 'data/default'])
    ], 
    install_requires=['six', 'requests', 'psutil', 'evalidate'],
    include_package_data = True,
    zip_safe=False
)    

