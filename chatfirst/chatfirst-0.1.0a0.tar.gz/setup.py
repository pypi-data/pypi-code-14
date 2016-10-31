from setuptools import setup
setup(
  name='chatfirst',
  version='0.1.0a',
  description='Chatfirst Python Client',
  author='Ivan Tertychnyy',
  author_email='it@chatfirst.co',
  packages=['chatfirst'],
  url='https://github.com/chatfirst/chatfirst',
  license='LICENSE.txt',
  install_requires=[
        "requests>=2.10.0",
    ],
)
