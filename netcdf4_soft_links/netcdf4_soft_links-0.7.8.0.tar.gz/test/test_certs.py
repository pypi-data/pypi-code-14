import os
import requests
import pydap.lib

headers = {
    'user-agent': pydap.lib.USER_AGENT,
            'connection': 'close'}
url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
#url='http://aims3.llnl.gov/thredds/dodsC/cmip5_css02_data/cmip5/output1/NCAR/CCSM4/amip/day/atmos/day/r4i1p1/tas/1/tas_day_CCSM4_amip_r4i1p1_19790101-20101231.nc'
session=requests.Session()
X509_PROXY=os.environ['X509_USER_PROXY']
resp=session.get(url,
                     cert=X509_PROXY,allow_redirects=True,headers=headers)
                     #cert=(X509_PROXY,X509_PROXY),allow_redirects=True,headers=headers,verify=False)
if resp.status_code==401:
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}
    data={'openid_identifier':'https://ceda.ac.uk/openid/'}
    resp=session.get(url,allow_redirects=True,headers=headers,params=data)
    print(resp.headers)
    print(resp.status_code)
    #print(resp.text)

