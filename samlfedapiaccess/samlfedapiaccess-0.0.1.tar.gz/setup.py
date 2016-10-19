from setuptools import setup
 
setup(
    name = 'samlfedapiaccess',
    version = '0.0.1',
    description = 'SAML federated API access for AWS',
    author='NR',
    author_email='neeharika.mm@gmail.com',
    url='https://github.com/youraccount/foolib',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
	install_requires=['beautifulsoup4','requests','html5lib','boto'],
	scripts=['FederatedAPIAccess-Python2.7.py']
)
