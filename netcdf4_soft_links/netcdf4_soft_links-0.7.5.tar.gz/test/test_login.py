import requests
import pydap.lib

url='https://ceda.ac.uk/OpenID/Provider/login'
session=requests.Session()
#resp=session.get(url,allow_redirects=True)
#print(resp.status_code)
payload={'username':'flaliberte','password':'Salut1001',
         'submit':'Login',
         'success_to':'https://ceda.ac.uk/OpenID/Provider/home',
         'fail_to':'https://ceda.ac.uk/OpenID/Provider/login'
         }
resp=session.post(url,data=payload,allow_redirects=True)
print(resp.text)
print(resp.status_code)



headers = {
    'user-agent': pydap.lib.USER_AGENT,
        'connection': 'close'}
url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
resp=session.get(url,allow_redirects=True,headers=headers)
print(resp.status_code)
