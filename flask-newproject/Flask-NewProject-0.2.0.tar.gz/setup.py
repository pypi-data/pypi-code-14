from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()
    
setup(name='Flask-NewProject',
      version='0.2.0',
      description = 'Create new Flask project.',
      long_description = readme(),
      url='https://github.com/Gunak/Flask-NewProject/',
      classifiers = [
          'Development Status :: 1 - Planning',
          'Framework :: Flask',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
        ],
      author='Raymond Williams',
      author_email='Raymond.n.williams86@gmail.com',
      license='MIT',
      packages=['Flask_NewProject'],
#      install_requires=[
#          'flask',
#        ],
      entry_points = {
          'console_scripts': ['flask-skeleton=Flask_NewProject.skeleton:skeleton',
                              'flask-simple=Flask_NewProject.simple:simple']
        },
      zip_safe=False)
