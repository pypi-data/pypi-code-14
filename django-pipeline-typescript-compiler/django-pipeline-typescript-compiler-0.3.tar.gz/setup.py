from setuptools import setup

setup(
  name='django-pipeline-typescript-compiler',
  packages=['pipeline_typescript'],
  version='0.3',
  description='Django Pipeline Compiler for Typescript',
  long_description='This project is a fork from the original django-pipeline-typescript plugin',
  author='Jonathan ZIMPFER',
  author_email='jonathan.zimpfer@gmail.com',
  url='https://github.com/ponkt/django-pipeline-typescript',
  download_url='https://github.com/ponkt/django-pipeline-typescript/tarball/0.3',
  keywords=['pipeline', 'assets', 'typescript'],
  classifiers=[
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Framework :: Django",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
  ],
  install_requires=[
    'django_pipeline>=1.6.0'
  ]
)
