from setuptools import setup

setup(name='qlda',
      version='0.1.6',
      description='Lda-MLOPE',
      url='https://github.com/Quangbd/qlda',
      author='Quang Bui Duc',
      author_email='quangbd.hust@gmail.com',
      license='NONE',
      packages=['qlda'],
      install_requires=[
          'numpy', 'scipy',
      ],
      zip_safe=False)
