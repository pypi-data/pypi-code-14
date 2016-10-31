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

# How mature is this project? Common values are
#   3 - Alpha
#   4 - Beta
#   5 - Production/Stable

classifier = [
                "Programming Language :: Python",
                'Development Status :: 3 - Alpha', 
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: MIT License',
                'Natural Language :: English',
                'Operating System :: Unix',
                'Programming Language :: Python :: 3 :: Only'
             ] 

keywords='ruxi tools ruxitools xydb intermediate data containers',
    
# setup   
setup(
      name='ruxitools'
    , version="0.2.2"
    , description="Misc general use functions. XyDB: container fo intermediate data. "
    , url="http://github.com/ruxi/tools"
    , author="ruxi"
    , author_email="ruxi.github@gmail.com"
    , license="MIT"
    , packages=['ruxitools']
    , tests_require=tests_require
    , test_suite= 'nose.collector'
    , classifiers = classifier
    , keywords=keywords
    )