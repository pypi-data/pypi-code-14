from distutils.core import setup
setup(name='ChineseWordFinder',
      version='1.0.0',
      keywords=('word', 'segmenetation', 'summerize'),
      description='Find Chinese Words',
      license = 'MIT License',
      author='huashenger',
      author_email='xueerpeng2014@163.com',
      url= ' ',
      packages=['ChineseWordFinder'],
      package_dir={'ChineseWordFinder':'ChineseWordFinder'},
      package_data={'yaha':['*.*','analyse/*','dict/*']}
)
