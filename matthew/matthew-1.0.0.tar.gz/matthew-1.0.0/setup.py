from setuptools import setup, find_packages

setup(name='matthew',
      version='1.0.0',
      description='Matthew',
      author='Matthew',
      author_email='automatthew@gmail.com',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      install_requires=[
      ],
      zip_safe=False)
