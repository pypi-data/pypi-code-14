import setuptools


setuptools.setup(name='stupidjoke',
                 version='0.1.1',
                 description='The most stupid joke in the world',
                 url='http://github.com/pannkotsky/stupidjoke',
                 author='Valerii Kovalchuk',
                 author_email='kovvalole@gmail.com',
                 license='MIT',
                 packages=['stupidjoke'],
                 install_requires=[
                           'markdown',
                       ],
                 zip_safe=False)
