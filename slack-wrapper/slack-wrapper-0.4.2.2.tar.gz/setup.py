from setuptools import setup

setup(
  name='slack-wrapper',
  packages=['slack_wrapper'],
  install_requires=[
    'requests',
    'websocket-client'
  ],
  version='0.4.2.2',
  description='A wrapper for the slack API and RTM',
  author='therightman',
  author_email='therightmandev@gmail.com',
  url='https://github.com/therightmandev/slack-wrapper',
  license='MIT',
  download_url='https://github.com/therightmandev/slack-wrapper/tarball/0.4.2.2',
  keywords=['slack', 'api', 'bot', 'bots'],
  classifiers=[],
)
