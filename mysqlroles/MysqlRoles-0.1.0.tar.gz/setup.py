from distutils.core import setup

setup(name='MysqlRoles',
      version='0.1.0',
      description='Role Managment for Mysql',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 1 - Planning', 'Topic :: Database',
                   'Intended Audience :: Information Technology', 'Programming Language :: SQL', 'Programming Language :: Python :: 2.7'],
      long_description=open('README.md', 'r').read(),
      packages=['MysqlRoles'],
      )
