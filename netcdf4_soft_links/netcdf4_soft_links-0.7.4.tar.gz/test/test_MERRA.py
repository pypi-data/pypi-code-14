import mechanize

#base_url = 'http://goldsmr3.gesdisc.eosdis.nasa.gov:80/opendap/MERRA_MONTHLY/MAIMCPASM.5.2.0/1979/MERRA100.prod.assim.instM_3d_asm_Cp.197901.hdf'
base_url = 'https://urs.earthdata.nasa.gov/'

br = mechanize.Browser()
#br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

r = br.open(base_url)
html = r.read()

br.select_form(nr=0)

br.form['username']='flaliberte'
br.form['password']='Salut1001'

r=br.submit()

html=r.read()
print(html)
br.close()
