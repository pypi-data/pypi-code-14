import requests
import pydap.lib
from bs4 import BeautifulSoup

username='flalib'
openid='https://pcmdi.llnl.gov/esgf-idp/openid/'
url='https://pcmdi.llnl.gov/openid/login/'
#url'https://esgf-index1.ceda.ac.uk/openid/login/'
session=requests.Session()
#resp=session.get(url,allow_redirects=True)
resp=session.get(url)
csrftoken = session.cookies['csrftoken']

payload={'openid_identifier':openid+'flalib', 'csrfmiddlewaretoken':csrftoken}
#payload={}
#for input in inputs:
#    name=input.get('name')
#    value=input.get('value')
#    if name=='openid_identifier':
#        payload.update({name:openid})
#    elif input.get('type') != 'submit':
#        payload.update({name:value})
print(payload)
resp=session.post(url,data=payload,allow_redirects=True,headers=dict(Referer=url))

soup=BeautifulSoup(resp.text,'lxml')
form = soup.find('form')
auth_url=form.get('action')
inputs = form.find_all('input')
payload={}
for input in inputs:
    name=input.get('name')
    value=input.get('value')
    payload.update({name:value})
print(payload)

resp=session.post(auth_url,data=payload,allow_redirects=True,headers=dict(Referer=url))
soup=BeautifulSoup(resp.text,'lxml')
form=soup.find('form')
print(auth_url)
submit_url=form.get('action')
if submit_url[0]=='/':
    submit_url='/'.join(auth_url.split('/')[:4])+submit_url
print(submit_url)

inputs = form.find_all('input')
payload={'password':'Salut1001!'}

#resp=session.post(submit_url,data=payload,allow_redirects=True,headers=dict(Referer=url))
resp=session.post(submit_url,data=payload,allow_redirects=True,headers=dict(Referer=url))
print(resp.text)
quit()
headers = {
    'user-agent': pydap.lib.USER_AGENT,
        'connection': 'close'}
url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
resp=session.get(url,allow_redirects=True,headers=headers)
print(resp.status_code)
