#coding:utf-8
'''
# Anonymous use have limit on each API calling access 100/day
# Please Login Your Account to deepnlp.org to increase API calling limit
'''
# Login to Default User of Pypi for Demo Purpose
import sys
import requests, urllib

#base_url = "www.deepnlp.org"
#username = 'pypi_default'
#password = 'pypi_passw0rd'

base_url = 'http://10.10.12.251:5000'
username = 'pypi_default'
password = 'pypi_passw0rd'

credentials = {'username' : username, 'password' : password}
login_url = base_url + '/account/login/'
login_cookie = requests.post(login_url, data=credentials)
secure_cookie = login_cookie.cookies # save cookie for future use


# Calling DeepNLP API of www.deepnlp.org
# Segmentation
text = "我想吃北京烤鸭"
text = text.decode(sys.stdin.encoding).encode("utf-8") # text coding to utf-8
url_segment = base_url + "/api/v1.0/segment/?" + "text=" + urllib.quote(text)
web = requests.get(url_segment, cookies = secure_cookie)
print (web.text)


# POS tagging
text = "我想吃北京烤鸭"
text = text.decode(sys.stdin.encoding).encode("utf-8") # text coding to utf-8
url_pos = base_url + "/api/v1.0/pos/?" + "text=" + urllib.quote(text)
web = requests.get(url_pos, cookies = secure_cookie)
print (web.text)


# NER tagging
text = "我想吃北京烤鸭"
text = text.decode(sys.stdin.encoding).encode("utf-8") # text coding to utf-8
url_ner = base_url + "/api/v1.0/ner/?" + "text=" + urllib.quote(text)
web = requests.get(url_ner, cookies = secure_cookie)
print (web.text)

# Pipeline 
text = "我想吃北京烤鸭"      # text to parse
text = text.decode(sys.stdin.encoding).encode("utf-8") # text coding to utf-8
annotators = "segment,ner"   # moduels to return
url_pipeline = base_url + "/api/v1.0/pipeline/?" + "text=" + urllib.quote(text) + "&annotators=" + urllib.quote(annotators)
web = requests.get(url_pipeline, cookies = secure_cookie)
print (web.text)




