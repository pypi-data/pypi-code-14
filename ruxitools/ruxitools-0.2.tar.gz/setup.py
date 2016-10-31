from setuptools import setup
import sys 

if sys.version_info[:2]<(3,5):
    sys.exit("ruxitools requires python 3.5 or higher")
    
# defining variables
install_requires = []

tests_require = [
                      'mock'
                    , 'nose'
                ]
classifier = [
                "Programming Language :: Python"
             ] 
    
# setup   
setup(
      name='ruxitools'
    , version="0.2"
    , description="Misc general use functions. XyDB: container fo intermediate data. "
    , url="http://github.com/ruxi/tools"
    , author="ruxi"
    , author_email="ruxi.github@gmail.com"
    , license="MIT"
    , packages=['ruxitools']
    , tests_require=tests_require
    , test_suite= 'nose.collector'
    , classifiers = classifier
    )