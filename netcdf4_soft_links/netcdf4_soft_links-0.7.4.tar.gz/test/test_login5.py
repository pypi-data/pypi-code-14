import requests
import mechanize
import cookielib
import urllib

def get_cookies(openid,password):
    issuer_node='/'.join(openid.split('/')[:3]).replace('http:','https:')

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    base_url=issuer_node+'/esg-orp/j_spring_openid_security_check.htm?openid_identifier='+urllib.quote_plus(openid)

    r = br.open(base_url)
    html = r.read()

    br.select_form(nr=0)

    br.form['password']=password
    br.submit()
    return cj

if __name__=='__main__':
    openid='https://pcmdi.llnl.gov/esgf-idp/openid/flalib'
    password='Salut1001!'
    #url='http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CCCma/CanAM4/amip/fx/atmos/fx/r0i0p0/v1/orog/orog_fx_CanAM4_amip_r0i0p0.nc.html'
    url='http://aims3.llnl.gov/thredds/dodsC/cmip5_css02_data/cmip5/output1/NCAR/CCSM4/amip/day/atmos/day/r4i1p1/tas/1/tas_day_CCSM4_amip_r4i1p1_19790101-20101231.nc.html'
    
    session=requests.Session()
    cookies=get_cookies(openid,password)
    resp=session.get(url,allow_redirects=True)
    print(resp.text)

