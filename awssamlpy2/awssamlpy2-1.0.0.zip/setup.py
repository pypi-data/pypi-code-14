from setuptools import setup
 
setup(
    name = 'awssamlpy2',
    version = '1.0.0',
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
