#################################################
#   My own Spider Implemetation
#################################################
import requests
from bs4 import BeautifulSoup
import pdb
from fake_useragent import UserAgent
ua = UserAgent()
"""
==================================
This will return info detaios as list of directory

Siup inthe input soup version of HTML

Xpath is the rot CSS selector for the eachelemts

info is a dircetory where key is the name and value is
attaribute for that elemnet

info2 is second layer depth in the below formar
{'url':['second css selctor','test'], ... }

It will return a list of dictory as pass in info

Example:

getAttrListForXPath(soup,"li.question .entry > a",info)


"""
def mget(s,t):
    if(t == 'text'):
        return s.text
    else:
        return s.get(t)
    
def getAttrListForXPath(soup, xpath, info = None, info2 = None):
    try:
        details =[]
        for x in soup.select(xpath):
            val  ={}
            if info != None:
                for k,v in info.items():
                    val[k] = mget(x,v)
            if info2 != None:
                #pdb.set_trace()
                for k,v in info2.items():
                    y = x.select(v[0])
                    val[k] = [ mget(t,v[1]) for t in y ]
                    
            details.append(val)
        return details
    except:
        return []
            
def buildSoup(url):
    try:
        headers = {'User-Agent': ua.random}
        print '[INFO]  Processing '+url
        data = requests.get(url).text
        return BeautifulSoup(data, 'html.parser')
    except:
        return None

#This test for Careercup only.
def test():
    #Parsing pages and 
    data = requests.get("https://careercup.com/page?pid=google-interview-questions").text
    soup = BeautifulSoup(data, 'html.parser')

    #Process ing pages and retive info list..
    post_urls  = []
    for i in range(1,10):
        u = 'https://careercup.com/page?pid=google-interview-questions&n='+str(i)
        soup = buildSoup(u)

        info ={'url':'href'}
        p = getAttrListForXPath(soup,"li.question .entry > a",info)
        #print p
        post_urls += [ 'https://careercup.com' + pp.get('url') for pp in p]
    #print post_urls


    #Parsing each artical link...
    all_post =[]
    for u in post_urls:
        #make soup
        soup = buildSoup(u)
        if soup == None:
            break;
        data = getAttrListForXPath(soup, '#question_preview',None,{'qn':['.entry p','text']})
        all_post.append(data[0]) #it will return a list


        
    #Write into the file..
    fo = open("foo.txt", "w+")
    ii =0
    for p in all_post:
        ii = ii+1
        sep = '\n\n'+str(ii)+".  "+'*'*50+'*'*50+'\n\n'
        fo.write(p.get('qn')+sep)
    fo.close()