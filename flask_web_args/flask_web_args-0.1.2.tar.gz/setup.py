from setuptools import setup

setup(name='flask_web_args',
      version='0.1.2',
      description='A library to help easily parse/validate web arguments with Flask',
      keywords='flask arguments args param params web app',
      url='https://github.com/ftheo/flask-web-args.git',
      author='Filippos Theodorakis',
      author_email='ftheo3@gmail.com',
      license='MIT',
      packages=['flask_web_args'],
      install_requires=[
          'flask',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
