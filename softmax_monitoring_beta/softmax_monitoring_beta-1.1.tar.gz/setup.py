from distutils.core import setup

setup(
	name='softmax_monitoring_beta',
	packages=['softmax_monitoring'],
	version='1.1',
	description='Beta release of softmax monitoring software',
	author='softmax',
	install_requires=[
        'requests', 'unirest'
    ],
	author_email='softmax.vision@gmail.com',
	url='https://github.com/softmax-vision/softmax_monitoring',
	download_url='https://github.com/softmax-vision/softmax_monitoring/archive/1.1.tar.gz',
	keywords=[],
	classifiers=[]
)
