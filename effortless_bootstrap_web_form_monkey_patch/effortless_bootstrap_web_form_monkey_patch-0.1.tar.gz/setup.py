from setuptools import setup

def readme():
  try:
    import pypandoc
    return pypandoc.convert('README.md', 'rst')
  except ImportError:
    return open('README.md').read()

setup(name='effortless_bootstrap_web_form_monkey_patch',
      version='0.1',
      description='Patch the old Form classes in web.py to create Bootstrap-compatible forms',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
      ],
      url='http://github.com/jmcguire/effortless_bootstrap_web_form_monkey_patch',
      author='Justin McGuire',
      author_email='jm@landedstar.com',
      keywords='web form bootstrap',
      license='MIT',
      packages=['effortless_bootstrap_web_form_monkey_patch'],
      install_requires=[
        'web.py',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

