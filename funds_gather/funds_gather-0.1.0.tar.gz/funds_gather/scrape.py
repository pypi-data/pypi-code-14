import requests
from lxml import html
import logging

session_requests = requests.session()

class CollegeSavingsMD(object):

    urls = { 'home': 'https://secure.collegesavingsmd.org/pls/prod/twpkwbis.P_WWWLogin',
             'login': 'https://secure.collegesavingsmd.org/pls/prod/twpkwbis.P_ValLogin',
             'acct_summary': 'https://secure.collegesavingsmd.org/pls/prod/hwtkpage.P_HomePage',
             'acct_select': 'https://secure.collegesavingsmd.org/pls/prod/hwtkstmt.P_DispYearChoice',
             'transactions': 'https://secure.collegesavingsmd.org/pls/prod/hwtkstmt_MD.P_DispAcctStmt',
            }

    def __init__(self):
        self.session = requests.session()
        pass

    def login(self, user, password):
        authenticity_token = self.get_form_key(self.urls['home'])
        payload = { 'sid': 'vekanayake',
                    'PIN': 'lenn4844',
                    'VALSRCKEY': authenticity_token
                  }

        result = self.session.post( self.urls['login'],
                                        data = payload, 
                                        headers = dict(referer=self.urls['login'])
                                     )

    def get_accounts(self):
        url = self.urls['acct_select']

    def get_form_key(self, url):
        """ Extract the private key used to validate form submissions """
        result = self.session.get(url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='VALSRCKEY']/@value")))[0]
        return authenticity_token


login_url = "https://secure.collegesavingsmd.org/pls/prod/twpkwbis.P_WWWLogin"
result = session_requests.get(login_url)
print (result.text)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='VALSRCKEY']/@value")))[0]
print(authenticity_token)

login_url = 'https://secure.collegesavingsmd.org/pls/prod/twpkwbis.P_ValLogin'
payload = { 'sid': 'vekanayake',
            'PIN': 'lenn4844',
            'VALSRCKEY': authenticity_token
        }
    
result = session_requests.post(
        login_url, 
        data = payload, 
        headers = dict(referer=login_url)
        )

url = 'https://secure.collegesavingsmd.org/pls/prod/hwtkpage.P_HomePage'
result = session_requests.get(
        url, 
        headers = dict(referer = url)
        )
print (result.text)

url = 'https://secure.collegesavingsmd.org/pls/prod/hwtkstmt.P_DispYearChoice'
result = session_requests.get(
        url, 
        headers = dict(referer = url)
        )
print (result.text)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='VALSRCKEY']/@value")))[0]

print ("-----------------------\n")
print ("DOING TRANSACTIONS")
url = 'https://secure.collegesavingsmd.org/pls/prod/hwtkstmt_MD.P_DispAcctStmt'
payload = { 'cnum': '50224095',
            'trans': 'ALL',
            'taxyear': '',
            'fdate': '',
            'tdate': '',
            'callfrom': '',
            'VALSRCKEY': authenticity_token
            }
headers = { 'Refererer' : 'https://secure.collegesavingsmd.org/pls/prod/hwtkstmt_MDtkstmt.P_DispYearChoice',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/xml*;q=0.8',
            'Origin': 'https://secure.collegesavingsmd.org',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8',
            }
result = session_requests.post(
        url, 
        data = payload, 
        headers = dict(referer='https://secure.collegesavingsmd.org/pls/prod/hwtkstmt_MDtkstmt.P_DispYearChoice')
        )
print (result.content)
print (result.request.headers)
print (result.headers)
# Let's try doing an xpath query
with open('trans.txt', 'w') as f:
    f.write(result.content)
tree = html.fromstring(result.content)
