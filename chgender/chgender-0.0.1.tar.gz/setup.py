try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='chgender',
    version='0.0.1',
    description='Gender gusser for Chinese names in English (pinyin) form',
    keywords='gender name guess python',
    url='https://github.com/jiajianzhou/chgender',
    author='Jiajian Zhou',
    author_email='jiajianzhou0808@gmail.com',
    packages=['chgender'],
    package_data={'': ['LICENSE'],
                  'chgender': ['chinese_name_lib.txt','pinyin_dataset.txt']},
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    entry_points={
        'console_scripts': [
            'chg = chgender.batch:main',
        ],
    }
)
