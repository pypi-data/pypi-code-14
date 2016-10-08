import setuptools


def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(name='stupidjoke',
                 version='0.2',
                 description='The most stupid joke in the world',
                 url='http://github.com/pannkotsky/stupidjoke',
                 author='Valerii Kovalchuk',
                 author_email='kovvalole@gmail.com',
                 license='MIT',
                 packages=['stupidjoke'],
                 install_requires=[
                     'markdown',
                     'mock'
                 ],
                 entry_points={
                     'console_scripts':
                         ['stupid-joke=stupidjoke.cmd.stupid_joke:main']
                 },
                 zip_safe=False)
