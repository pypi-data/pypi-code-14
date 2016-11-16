from setuptools import find_packages,setup

setup(
    description='RFour Request Response Protocol',
    install_requires=[
        'arrow',
        'rask'
    ],
    license='https://gitlab.com/vikingmakt/rfour/raw/master/LICENSE',
    maintainer='Umgeher Torgersen',
    maintainer_email='me@umgeher.org',
    name='rfour',
    packages=find_packages(),
    url='https://gitlab.com/vikingmakt/rfour',
    version="0.0.4"
)
