from setuptools import setup

setup(
  name = 'xmppgcm',
  packages = ['xmppgcm'], # this must be the same as the name above
  version = '0.1',
  description = 'Client Library for Firebase Cloud Messaging using XMPP',
  install_requires=['sleekxmpp',],
  author = 'Winster Jose',
  author_email = 'wtjose@gmail.com',
  license='Apache License 2.0',
  url = 'https://github.com/winster/xmppgcm',
  keywords = ['gcm', 'fcm', 'xmpp', 'xmppgcm', 'xmppfcm'], # arbitrary keywords
  classifiers = [
		'Development Status :: 2 - Beta',
		'Intended Audience :: Developers',
    	'Topic :: Software Development :: Build Tools',
		'Programming Language :: Python :: 2.7',
  ],
)