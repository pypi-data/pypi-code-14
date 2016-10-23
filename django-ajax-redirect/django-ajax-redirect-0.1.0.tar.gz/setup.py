from setuptools import setup, find_packages

from ajax_redirect import __version__

version_str = ".".join(str(n) for n in __version__)

requires = ['django>=1.8']

setup(name='django-ajax-redirect',
      version=version_str,
      description='AJAX redirection middleware and decorator for Django',
      url='https://github.com/cvng/django-ajax-redirect',
      author='cvng',
      author_email='mail@cvng.io',
      license='MIT',
      packages=find_packages(),
      install_requires=requires,
      zip_safe=False,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          "Framework :: Django",
      ])
