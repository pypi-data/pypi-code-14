from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()
	f.close()

setup(name='save',
      version='0.1',
      description='A very simple module to safely save data to files in python',
      long_description=readme(),
      classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: System :: Filesystems',
      ],
      keywords='save data file path system',
      url='https://github.com/ndrbrt/save.py',
      author='Andrea Bertoloni',
      author_email='contact@andreabertoloni.com',
      license='MIT',
      packages=['save'],
      include_package_data=True,
      zip_safe=False)