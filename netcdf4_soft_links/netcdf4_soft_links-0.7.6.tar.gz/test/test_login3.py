import requests
import pydap.lib
from bs4 import BeautifulSoup

username='flalib'
openid='https://pcmdi.llnl.gov/esgf-idp/openid/flalib'
url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'

session=requests.Session()
resp=session.get(url,allow_redirects=True)

soup=BeautifulSoup(resp.text,'lxml')
form = soup.find('form')
auth_url=form.get('action')
if auth_url[0]=='/':
    auth_url='/'.join(url.split('/')[:4])+auth_url
resp=session.get(auth_url,allow_redirects=True)

check_url=resp.url.split('?')[0]
print(check_url+'?openid='+openid)
headers = {
    "User-Agent":
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
    "openid":openid
            }
resp=session.post(check_url,allow_redirects=True,headers=headers)
print(check_url+'?openid='+openid)
#url='https://pcmdi.llnl.gov/esgf-idp/idp/login.htm'
#resp=session.get(url,allow_redirects=True,headers=headers)
#print(resp.text)
#url='https://esgf-data1.ceda.ac.uk/esg-orp/j_spring_openid_security_check.htm?openid_identifier=https%3A%2F%2Fpcmdi.llnl.gov%2Fesgf-idp%2Fopenid%2Fflalib'
url='https://pcmdi.llnl.gov/esgf-idp/idp/openidServer.htm?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.claimed_id=https%3A%2F%2Fpcmdi.llnl.gov%2Fesgf-idp%2Fopenid%2Fflalib&openid.identity=https%3A%2F%2Fpcmdi.llnl.gov%2Fesgf-idp%2Fopenid%2Fflalib&openid.return_to=https%3A%2F%2Fesgf-data1.ceda.ac.uk%2Fesg-orp%2Fj_spring_openid_security_check.htm&openid.realm=https%3A%2F%2Fesgf-data1.ceda.ac.uk%2F&openid.assoc_handle=1469481824113-399&openid.mode=checkid_setup&openid.ns.ext1=http%3A%2F%2Fopenid.net%2Fsrv%2Fax%2F1.0&openid.ext1.mode=fetch_request&openid.ext1.type.email=http%3A%2F%2Fopenid.net%2Fschema%2Fcontact%2Finternet%2Femail&openid.ext1.type.firstname=http%3A%2F%2Fopenid.net%2Fschema%2FnamePerson%2Ffirst&openid.ext1.type.lastname=http%3A%2F%2Fopenid.net%2Fschema%2FnamePerson%2Flast&openid.ext1.required=email%2Cfirstname%2Clastname'
resp=session.get(url,allow_redirects=True,headers=headers)
#print(resp.text)

soup=BeautifulSoup(resp.text,'lxml')
form = soup.find('form')
auth_url=form.get('action')
if auth_url[0]=='/':
    auth_url='/'.join(resp.url.split('/')[:4])+auth_url
print(auth_url)
payload={'password':'Salut1001!'}
resp=session.post(auth_url,data=payload,allow_redirects=True,headers=dict(Referer=url))
print(resp.text)

url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
resp=session.get(url,allow_redirects=True,headers=headers)
print(resp.status_code)
quit()

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

resp=session.post(submit_url,data=payload,allow_redirects=True,headers=dict(Referer=url))
print(resp.text)
quit()
headers = {
    'user-agent': pydap.lib.USER_AGENT,
        'connection': 'close'}
url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
resp=session.get(url,allow_redirects=True,headers=headers)
print(resp.status_code)
