from distutils.core import setup
setup(
  name = 'DevIoTGateway',
  packages = ['DevIoTGateway'], # this must be the same as the name above
  version = '2.1',
  description = 'Quickly help user to build DevIot Gateway service',
  author = 'Tingxin Xu',
  author_email = 'tingxxxu@cisco.com',
  url = 'https://github.com/tingxin/DevIoT_Python_SDK', # use the URL to the github repo
  download_url = 'https://github.com/tingxin/DevIoT_Python_SDK/tree/master/DevIoTGateway',
  keywords = ['Gateway', 'DevIot', 'Cisco'],
  classifiers = [],
  install_requires=[
        "paho-mqtt"
    ]
)
