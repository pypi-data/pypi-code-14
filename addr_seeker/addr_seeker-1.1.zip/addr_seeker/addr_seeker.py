
from HTMLreader import HTMLreader
from HTMLreader import getHTML
from urllib.parse import urlparse
import re


#STATUS 
#   0: page does not exist
#   1: branches do not exist
#   2: addr does not exist in neither the page nor it`s branches
#   3: addr found in tree

MAX_LINKS_PER_SITE = pow(2, 32)

states = ['ak',  'alaska', 'al','alabama','ar','arkansas','as','american samoa','az','arizona',
  'ca', 'california', 'co', 'colorado', 'ct','connecticut','dc','district of columbia','de','delaware',
  'fl', 'florida', 'ga','georgia', 'gu', 'guam','hi', 'hawaii', 'ia','iowa','id', 'idaho', 'il','illinois',
  'in', 'indiana','ks', 'kansas', 'ky','kentucky','la','louisiana', 'ma', 'massachusetts', 'md', 'maryland',
  'me','maine', 'mi', 'michigan', 'mn', 'minnesota', 'mo', 'missouri', 'ms', 'mississippi', 'mt', 'montana',
  'nc', 'north carolina', 'nd', 'north dakota', 'ne','nebraska', 'nh','new hampshire', 'nj', 'new jersey',
  'nm', 'new mexico', 'nv', 'nevada', 'ny', 'new york', 'oh', 'ohio', 'ok','oklahoma', 'or', 'oregon',
  'pa', 'pennsylvania', 'pr', 'puerto rico', 'ri', 'rhode island', 'sc', 'south carolina', 'sd', 'south dakota',
  'tn', 'tennessee', 'tx', 'texas', 'ut', 'utah', 'va', 'virginia', 'vi', 'virgin islands', 'vt', 'vermont',
  'wa', 'washington', 'wi', 'wisconsin', 'wv', 'west virginia', 'wy', 'wyoming']
  

POBXregex = r"(p.?o.? ?box.? ?[0-9]+)"
STRTregex = r"([0-9]+ +[a-z][ a-z0-9#]{1,40}(?:[,\.][ a-z0-9]*)?)"
SEPSregex = r"[,\.]?\s+"

class AddrSeeker():
    URLregex = re.compile( #django server url regex
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?' 
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
    guideWords = ["contact", "location","address", "headquarter", #most probable links
                     "about", "info","support", #possible links
                     "faq", "branch", #lucky guess 
                       "relation"] #last resort #"customer service"
                     
    ADDRregex = re.compile(r"\s*(?:(?:"+STRTregex+SEPSregex+POBXregex+r")|(?:"+STRTregex+r"|"+POBXregex+r"))"+SEPSregex+ #street adr and pobox or either
    r"([a-z]+(?: [a-z]+){0,3})"+SEPSregex+ # city
    r"("+'|'.join(states)+r")"+SEPSregex+ # state
    r"([0-9]{5}(?:[\.,\- #]?[0-9]{4})?)\s*") #zip code
    
    def __init__(self, maxDepth):
        self._URLVisited = []
        self._url = ""
        self._maxDepth = maxDepth
        self._status = 0
        self._deepestDepth = 0
        self._reader = HTMLreader()
        
    def setUrl(self, url):
        self._url = url
            
    def findMailingAddr(self):
        self._status = 0
        self._deepestDepth = 0

        self._URLVisited = []
        R = self._findAddr(self._url, 0)

        if(R[0] == 3): # found an address
            return R
        else: # the last branch was returned
            return (self._status, None, self._deepestDepth) # return the largest status achieved and the biggest depth reached
        
    def _findAddr(self, url, depth):
        print(url, depth)
        #print(url)
        if(url[:4]!='http'):
            url = 'http://'+url
        doc = getHTML(url)
        if(doc == None):
            self._status = max(0, self._status)
            return (0, None, depth)
        self._deepestDepth = max(self._deepestDepth, depth)
        
        self._reader.reset()
        self._reader.feed(doc)
        address = AddrSeeker.scanText(self._reader.text)

        if(address != None):
            self._status = 3
            return (3, address, depth)
            
        elif(depth < self._maxDepth):# should continue searching in tree?
            links = self._reader.links
            branchesExist = False
            result = None
            
            for link in links:
                for guideWord in AddrSeeker.guideWords:
                    newUrl = self.constructURL(url, link[1])
                    if(guideWord in link[0] and (newUrl not in self._URLVisited)): #link is a branche
                        self._URLVisited +=newUrl #mark as visited
                        R = self._findAddr(newUrl, depth+1) #search in branch
                        
                        if(R[0] != 0): #valid branch
                            branchesExist= True
                        if(R[0]==3): #branch returned an address
                            #return R
            #####################################################################################################
                            #the following code implements bredth first search (takes too much time)            #
                            #if you wish to make this faster using depth first set                              #
                            #simply delete this block and uncomment return R on line 108                        #
                            if R[2]==depth+1: #address cannot be shallower                                      #
                                return R                                                                        #
                            elif result == None or R[2] < result[2]:#address may be shallower in other branches #
                                result = R #save result in case this is the shallowest result                   #
                                                                                                                #
                                                                                                                #
            if result != None: #something was found in the branches                                             #
                return result                                                                                   #
            #####################################################################################################
            if branchesExist: #branches exist with no address in them
                self._status = max(2, self._status)
                return (2, None, depth)
                
        #branches do not exist or end of visable tree reached(maxDepth)
        self._status = max(1, self._status)
        return (1, None, depth)
    
    def constructURL(self, Url, href):
        if href == None or href[:6]=='mailto' or href.isspace() or href[-4:] =='.pdf' or href[-3:]==".js" or "javascript" in href:
            return ''
        if Url == None:
            Url = ''
        parsed_uri = urlparse( Url)
        Url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        href = re.sub('\A(?:/{0,2}\.+)+', '', href)
        if href[:4] == 'http':
            return href
        elif href[:2] == '//':
            return 'http:'+href
        elif href[:3] == 'www':
            return 'http://'+href
        elif len(href)>0 and href[0] == '/':
            return Url+href[1:]
        else:
            return Url+href
    @staticmethod
    def scanText(text):
        Addr = AddrSeeker.ADDRregex.search(text)
        if Addr == None:
            return None
        
        else:
            a =Addr.groups() 
            STRT = a[0] if a[0]!=None else a[2]
            POBX = a[1] if a[1]!=None else a[3]
            City =  a[4]
            State = a[5]
            Zipc = a[6]
            return (STRT, POBX, City, State, Zipc)
        
    @staticmethod
    def isValidURL(addr):
        parsed = urlparse(addr)
        return bool(parsed)
