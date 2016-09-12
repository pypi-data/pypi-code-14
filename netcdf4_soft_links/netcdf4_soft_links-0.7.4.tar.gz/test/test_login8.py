import requests
import netcdf4_soft_links.remote_netcdf as remote_netcdf
cred={'username': None, 'openid': 'https://esgf-data.dkrz.de/esgf-idp/openid/flaliberte', 'password': 'Salut1001!', 'use_certificates': False}
url=[u'http://cordexesg.dmi.dk/thredds/dodsC/cordex_general/cordex/output/EUR-11/DMI/ICHEC-EC-EARTH/historical/r3i1p1/DMI-HIRHAM5/v1/day/pr/v20131119/pr_EUR-11_ICHEC-EC-EARTH_historical_r3i1p1_DMI-HIRHAM5_v1_day_19960101-20001231.nc', u'OPENDAP']

session=requests.Session()
print(remote_netcdf.remote_netCDF(url[0],url[1],session=session,**cred).is_available(num_trials=1))
