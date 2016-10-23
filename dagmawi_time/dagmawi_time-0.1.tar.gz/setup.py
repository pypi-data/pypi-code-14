from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='dagmawi_time',
      version='0.1',
      description='Create/modify an instance of time',
      long_description = "This package allows a developer to instantiate a time object and inc/dec the different time elements(sec,min,hour) as they wish",
      classifiers=[
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research'
          ,'Natural Language :: English'
          ,'Operating System :: MacOS'
          ,'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      author='Dagmawi Mulugeta',
      author_email='djdg432@gmail.com',
      license='None',
      packages=['dagmawi_time'],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )