from setuptools import setup

setup(
	name			 = 'otpsecure',
	packages		 = ['otpsecure'],
	version			 = '1.0.5',
	description		 = "OtpSecure's Python SDK",
	author			 = 'OtpSecure',
	author_email	 = 'sistemas@ecertic.com',
	url				 = 'https://github.com/ecertic/otpsecure_pyton-sdk',
	download_url	 = 'https://github.com/ecertic/otpsecure_pyton-sdk/tarball/1.0.5',
	keywords		 = ['otpsecure', 'sms'],
	install_requires = ['requests>=2.4.1','pycrypto>=2.6.1','beautifulsoup4'],
	license			 = 'BSD-2-Clause',
)