from setuptools import setup, find_packages
import vat_moss

setup(
    name='french_vat_moss',
    version=vat_moss.__version__,

    description='Tools for VAT MOSS and Norway VAT on digital services.',
    long_description='Fork of https://github.com/wbond/vat_moss-python'
                     'Docs for this project are maintained at https://github.com/wbond/vat_moss-python#readme.',


    url='https://github.com/laurentL/vat_moss-python',

    author='Labatut Laurent',
    author_email='laurent@labatut.net',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='french vat',

    packages=find_packages(exclude=['tests*']),
    install_requires=['money', 'pythonsol']
)
