import requests
import netcdf4_pydap
cred={'username': 'flaliberte', 'password': 'Salut1001', 'use_certificates': False, 'authentication_url':'https://urs.earthdata.nasa.gov/'}
url = 'http://goldsmr3.gesdisc.eosdis.nasa.gov:80/opendap/MERRA_MONTHLY/MAIMCPASM.5.2.0/1979/MERRA100.prod.assim.instM_3d_asm_Cp.197901.hdf'

session=requests.Session()
import matplotlib.pyplot as plt
import numpy as np
with netcdf4_pydap.Dataset(url,session=session,**cred) as dataset:
    data = dataset.variables['SLP'][0,:,:]
    plt.contourf(np.squeeze(data))
    plt.show()

