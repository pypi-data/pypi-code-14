from distutils.core import setup

setup(
    name='pyzipit',
    version='0.0.5',
    packages=[
        'zip_by_address',
        'zip_by_address.zip_by_address_localizations',
        'zip_by_address.zip_by_address_localizations.israel',
        'zip_by_address.address_by_coordinates',
        'zip_by_address.address_by_coordinates.address_by_coordinates_localizations',
        'zip_by_address.address_by_coordinates.address_by_coordinates_localizations.israel',
        'zip_by_address.coordinates_by_address',
    ],
    url='https://github.com/asherbar/pyzipit/tarball/0.0.5',
    license='MIT',
    author='asherbar',
    author_email='asherbare@gmail.com',
    description='A Python library that provides tools for ZIP (as in "Zone Improvement Plan") related subjects'
)
