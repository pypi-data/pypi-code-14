from setuptools import setup

setup(name='okerrclient',
    version='2.0.7',
    description='client for okerr cloud monitoring system',
    url='http://okerr.com/',
    author='Yaroslav Polyakov',
    author_email='xenon@sysattack.com',
    license='MIT',
    packages=['okerrclient'],
    scripts=['scripts/okerrclient'],
    data_files = [
        ('okerrclient',['data/conf/okerrclient.conf']),
        ('/etc/init.d', ['data/init.d/okerrclient']),
        ('/etc/systemd/system',['data/systemd/okerrclient.service']),
    ], 
    install_requires=['six', 'requests', 'psutil', 'evalidate', 'python-daemon', 'configargparse'],
    include_package_data = True,
    zip_safe=False
)    

