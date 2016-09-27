from setuptools import setup

setup(name='django-userplus',
      version='0.3.2.8',
      description='Extended Auth User module for Django',
      url='https://github.com/ifedapoolarewaju/django-userplus.git',
      author='Ifedapo Olarewaju',
      author_email='ifedapoolarewaju@gmail.com',
      license='MIT',
      packages=['userplus', 'userplus.lib', 'userplus.static'],
      install_requires=['Django>=1.9', 'facebook-sdk>=2.0.0'],
      include_package_data=True,
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Framework :: Django'
      ],
      zip_safe=False)
