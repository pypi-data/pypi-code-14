from distutils.core import setup

from setuptools.command.install import install

class CustomInstall(install):

    def run(self):
        import os
        #os.system('bash get_data.sh')
        install.run(self)


setup(
    name='demographer',
    version='0.1.3',
    author='Josh Carroll, Mark Dredze and R. Knowles',
    author_email='mdredze@cs.jhu.edu',
    packages=['demographer'],
    package_dir={'demographer': 'demographer'},
    package_data={'demographer': ['data/*']},
    include_package_data=True,
    url='https://bitbucket.org/mdredze/demographer',
    download_url = 'https://bitbucket.org/mdredze/demographer/get/0.1.3.zip',
    license='LICENSE.txt',
    description='Extremely simple name demographics for Twitter names',
    install_requires=[
        "numpy >= 1.6.1",
        "scipy >= 0.9",
        "scikit-learn >= 0.16.1",
        "ujson >= 1.0.0",
    ],
    cmdclass={'install': CustomInstall},
)

