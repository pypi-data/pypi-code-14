import requests
import mechanize
import cookielib
import urllib
import ssl
import datetime
import os

from netcdf4_soft_links import esgf_pydap
from netcdf4_soft_links import esgf_http
from netcdf4_soft_links import esgf_get_cookies

if __name__=='__main__':
    #openid='https://pcmdi.llnl.gov/esgf-idp/openid/flalib'
    #password='Salut1001!'
    #openid='https://ceda.ac.uk/openid/Frederic.Laliberte'
    #username='flaliberte'
    #password='Salut1001'

    openid='https://esgf-data.dkrz.de/esgf-idp/openid/flaliberte'
    password='Salut1001!'

    url_list=[
    'http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc',
    'http://esgf-data1.diasjp.net/thredds/dodsC/esg_dataroot/cmip5/output1/MRI/MRI-CGCM3/amip/fx/atmos/fx/r0i0p0/v20110831/orog/orog_fx_MRI-CGCM3_amip_r0i0p0.nc',
    'http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/NCAR/CCSM4/amip/fx/atmos/fx/r0i0p0/v20130312/orog/orog_fx_CCSM4_amip_r0i0p0.nc',
    'http://esgf2.dkrz.de/thredds/dodsC/cmip5/output1/NCAR/CCSM4/amip/fx/atmos/fx/r0i0p0/v20130312/orog/orog_fx_CCSM4_amip_r0i0p0.nc',
    'http://aims3.llnl.gov/thredds/dodsC/cmip5_css02_data/cmip5/output1/NCAR/CCSM4/amip/day/atmos/day/r1i1p1/tas/1/tas_day_CCSM4_amip_r1i1p1_19790101-20101231.nc',
    ]
    cj=esgf_get_cookies.cookieJar(url_list[0],openid,password)
    quit()
    
    session=requests.Session()
    for url in url_list:
        print(url)
        time_start=datetime.datetime.now()
        with esgf_pydap.Dataset(url,session=session,openid=openid,password=password,username=username) as dataset:
            print(dataset)
            print(len(session.cookies))
            print(datetime.datetime.now()-time_start)

    session=requests.Session()
    for url in url_list:
        print(url)
        time_start=datetime.datetime.now()
        with esgf_http.Dataset(url.replace('dodsC','fileServer'),session=session,openid=openid,password=password,username=username) as dataset:
            size_string=dataset.wget(os.path.basename(url))
            print(size_string)
            print(len(session.cookies))
            print(datetime.datetime.now()-time_start)



