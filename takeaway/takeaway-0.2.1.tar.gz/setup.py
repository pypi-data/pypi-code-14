from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='takeaway',
    version='0.2.1',
    description='Command line interface for takeaway.com websites',
    long_description=readme(),
    url='https://github.com/Ovvovy/TakeAway',
    author='Ovv',
    author_email='ovv@outlook.com',
    license='MIT',
    packages=['takeaway', 'takeaway.basket', 'takeaway.database', 'takeaway.scrapper', 'takeaway.user'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['takeaway=takeaway.command_line:main']
    },
    install_requires=['beautifulsoup4==4.5.1', 'progressbar2==3.10.0', 'PTable==0.9.2', 'requests==2.10.0',
                      'SQLAlchemy==1.0.14'],
    include_package_data=True,
)
