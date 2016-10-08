from setuptools import setup,find_packages
p=find_packages()
print str(p)

setup(
    name='gt-push-sdk',
    version='4.0.1.1',
    author='getui',
    author_email='gtpushsdk@gmail.com',
    url='http://www.getui.com/',
    packages=find_packages(),
    keywords='getui push gtpush',
    description='getui push sdk for python'
)