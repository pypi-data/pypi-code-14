from distutils.core import setup

setup(
    name='xcute',
    version='0.0.1',
    packages=['xcute', 'xcute.templates'],
    url='https://github.com/schwa/xcute',
    license='MIT',
    author='schwa',
    author_email='jwight@mac.com',
    description='xcode utilitiy', # TODO: flush this out
    keywords=['build', 'xcode', 'iOS', 'cocoa', 'macOS'],
    platform="MacOS X",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Build Tools',
    ],
    install_requires=[
        'click',
        'click_didyoumean',
        'jinja2',
        'memoize',
        'pathlib2',
        'six',
    ],
    entry_points='''
    [console_scripts]
    xcute=xcute.main:xcute_cli
    ''', )
