from setuptools import setup
 
setup(
    name = 'awssamllinux',
    version = '0.0.1',
    description = 'SAML federated API access for AWS',
    author='Neeharika',
    author_email='neeharika.mm@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
    ],
	install_requires=['beautifulsoup4','requests','html5lib','boto'],
	scripts=['aws-saml.py']
)
