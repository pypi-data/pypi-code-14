import requests
#import netcdf4_soft_links.remote_netcdf as remote_netcdf
import netcdf4_soft_links.esgf_pydap as esgf_pydap
cred={'username': None, 'openid': 'https://esgf-data.dkrz.de/esgf-idp/openid/flaliberte', 'password': 'Salut1001!', 'use_certificates': False}
url=[u'http://cordexesg.dmi.dk/thredds/dodsC/cordex_general/cordex/output/EUR-11/DMI/ICHEC-EC-EARTH/historical/r3i1p1/DMI-HIRHAM5/v1/day/pr/v20131119/pr_EUR-11_ICHEC-EC-EARTH_historical_r3i1p1_DMI-HIRHAM5_v1_day_19960101-20001231.nc', u'OPENDAP']

session=requests.Session()
#import sys
#sys.setrecursionlimit(100)
import matplotlib.pyplot as plt
import numpy as np
with esgf_pydap.Dataset(url[0],session=session,**cred) as dataset:
    data = dataset.variables['pr'][0,:,:]
    plt.contourf(np.squeeze(data))
    plt.show()

