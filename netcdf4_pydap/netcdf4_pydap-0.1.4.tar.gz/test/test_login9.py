import requests
import netcdf4_pydap 
import netcdf4_pydap.esgf as esgf
openid = 'https://esgf-data.dkrz.de/esgf-idp/openid/flaliberte'
username = None
password = 'Salut1001!'

openid = 'https://ceda.ac.uk/openid/Frederic.Laliberte'
username = 'flaliberte'
password = 'Salut1001'
cred={
      'username': username,
      'password': password,
      'use_certificates': False, 
      'authentication_url': esgf.authentication_url(openid)}


url=[u'http://cordexesg.dmi.dk/thredds/dodsC/cordex_general/cordex/output/EUR-11/DMI/ICHEC-EC-EARTH/historical/r3i1p1/DMI-HIRHAM5/v1/day/pr/v20131119/pr_EUR-11_ICHEC-EC-EARTH_historical_r3i1p1_DMI-HIRHAM5_v1_day_19960101-20001231.nc', u'OPENDAP']

session=requests.Session()
import matplotlib.pyplot as plt
import numpy as np
with netcdf4_pydap.Dataset(url[0],session=session,**cred) as dataset:
    data = dataset.variables['pr'][0,:,:]
    plt.contourf(np.squeeze(data))
    plt.show()

