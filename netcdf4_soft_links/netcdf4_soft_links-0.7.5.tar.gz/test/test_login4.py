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
base_headers = {
    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    "Accept-Language":'en-US,en;q=0.8',
    "Accept-Encoding":'gzip, deflate, sdch, br',
    "Upgrade-Insecure-Requests":1,
            }
base_url='https://esgf-data1.ceda.ac.uk/esg-orp/j_spring_openid_security_check.htm?openid_identifier=https%3A%2F%2Fpcmdi.llnl.gov%2Fesgf-idp%2Fopenid%2Fflalib'
resp=session.get(base_url,headers=base_headers)
specific_headers=({'Host':'pcmdi.llnl.gov','Connection':'keep-alive'})
next_to_last_resp=resp.history[-1]

headers = {
    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    "Accept-Language":'en-US,en;q=0.8',
    "Accept-Encoding":'gzip, deflate, sdch, br',
    'Cache-Control':'max-age=0',
    'Host':'pcmdi.llnl.gov',
    'Connection':'keep-alive',
    'Cookie':next_to_last_resp.headers['Set-Cookie'].split(';')[0],
    "Upgrade-Insecure-Requests":1,
            }
resp=session.get(resp.url,headers=headers,allow_redirects=True,cookies=next_to_last_resp.cookies)

soup=BeautifulSoup(resp.text,'lxml')
form = soup.find('form')
auth_url=form.get('action')
if auth_url[0]=='/':
    auth_url='/'.join(resp.url.split('/')[:4])+auth_url
headers = {
    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    "Accept-Language":'en-US,en;q=0.8',
    "Accept-Encoding":'gzip, deflate, br',
    'Cache-Control':'max-age=0',
    "Content-Type":"application/x-www-form-urlencoded",
    'Host':'pcmdi.llnl.gov',
    'Origin':'https://pcmdi.llnl.gov',
    'Referer':auth_url,
    'Connection':'keep-alive',
    'Content-Length':'21',
    "Upgrade-Insecure-Requests":1,
            }

payload={'password':'Salut1001!'}
print(headers)
resp=session.post(auth_url,data=payload,headers=headers,allow_redirects=True,cookies=next_to_last_resp.cookies)
print(resp.headers)
print(resp)
quit()

final_url='https://esgf-data1.ceda.ac.uk/esg-orp/home.htm'
headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'en-US,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':next_to_last_resp.headers['Set-Cookie'].split(';')[0],
'Host':'esgf-data1.ceda.ac.uk',
'Referer':auth_url,
'Upgrade-Insecure-Requests':1,
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
resp=session.get(final_url,headers=headers,allow_redirects=True,cookies=next_to_last_resp.cookies)
quit()


headers = {
    'user-agent': pydap.lib.USER_AGENT}
url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
resp=session.get(url,allow_redirects=True,headers=headers)
quit()

headers = {
    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    "Accept-Language":'en-US,en;q=0.8',
    "Accept-Encoding":'gzip, deflate, sdch, br',
    'Host':'esgf-data1.ceda.ac.uk',
    "Upgrade-Insecure-Requests":1,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
            }
resp=session.get(base_url,headers=headers)
#print(resp.text)
quit()

url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc'
resp=session.get(url,allow_redirects=True,headers=headers)
print(resp.status_code)
quit()

