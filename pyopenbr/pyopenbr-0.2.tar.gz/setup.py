from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pyopenbr',
      version='0.2',
      description='Improved Python Wrapper for the OpenBR Command-line Tool.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='open biometrics openbr face recognition',
      url='https://github.com/ant0nisk/pyopenbr',
      author='Antonis Katzourakis',
      author_email='antonis.katzourakis@gmail.com',
      license='Apache License, Version 2.0',
      packages=['pyopenbr'],
      include_package_data=True,
      zip_safe=False)
