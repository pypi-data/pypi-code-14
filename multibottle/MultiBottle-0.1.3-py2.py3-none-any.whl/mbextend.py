#!/usr/bin/env python3
import re
import bottle
from bottle import request
from bottle import mako_template as template
from objdict import combiParse,ObjDict
try:
    from viewmodel import BaseView
except ImportError:
    BaseView= ObjDict
try:
    from siteSettings.site import paths
except ImportError:
    paths= lambda host:{'makoPath':['.']}
from .pages import NavPage

from collections import OrderedDict as ODict

class HtmlPage(NavPage):
    """ enhances page with screen stuff"""

    #now at this point....how is this different from just an instance of NavPage? (jan 2016)
    #routines here should either go to basicPage - or use other existing routines instead

    def __init__(self,req=None,view=None,*,post=None,table=None):
        """
        req is now defaulted to None, but actually view can be first paramter
        and is type checked so alternatve call is HtmlPage(view,**kwargs)

        """
        if isinstance(req,BaseView):
            req,view=None,req

        if req is None:
            req=ExtReq()
        if post is None:
            pass
        # self.postData=post

        if not hasattr(self,"flds"):self.flds=[]
        if not hasattr(self,"useDB"):self.useDB=0
        super().__init__(req,view=view)

        #self.template=self.hostInfo('fname')#.replace('.py','.html')

        if not hasattr(self,"table"):
            #not clear what table is.....looks like precursor to view
            self.table=table
        #self.getcooks(inSession=True)
        self.error=""
        #
    def appendToUrl(self,url,elist):
        return self.fixUrlGets(elist,url)

    def predraw(self,*args1,**args2): #2015 09 base method redundant?
        self.setSitePageData(*args1,**args2)
        #self.templateData['table']=self.table
        self.templateData['page']=self

    def checkAccess(self,codes):
        """ codes can be string...looks for any in the string """
        for code in list(codes):
            if code in self.access:
                return True
        return False



    def fixL(self,n,pageName=''):
        return self.fixUrlGets({'l':n},pageName=pageName)

def textPlainParse(txt):
    """ this is used to parse post data provided as plain text
    e.g.
    <fld1>=<val1>,<fld2>=<val2>
    <fld3>=<val3>
    """
    res=ODict()
    for line in txt.split('\n'):
        if line:
            key,dat=line.split('=',1)
            res[key]=dat.strip('\r')
    return res

class ExtReq:
    """ ExtReq is an extension of the bottle request, plus some adaptation to
    allow wider compatibility, including during the transition to bottle from
    the previous mod_python version
    see code of the init method for documenation on the various key information
    component, plus documenation with the various properties.

    Breakdown of the request.  e.g. (two examples)
    http://server.host.com:8080/Members/Cards/0?get=5
    http://server.host.com/Members/Stores/0/Product/6/

    *urlInSiteFull* would be Members/Cards/0 or Members/Stores/0/Products/0

    *urlInSite* would be Members/Cards   or Members/Stores/0/Products
    By default, the final numeric element is taken as an entry to
    'pageParms'. The 'setPageParms()' will move trailing elements of the url
    into the 'pageParms' dictionary. The default is simply to move the last
    trailing numberic if present, but using a pageParmsList can change that.
    See setPageParms().
    Pages can indicate that more of the URL is 'pageParms', and adjust from
    the default
    *pageParms* currently picks up a trailing 'index' paramter if present
    automatically, and may be upgraded to do more, but currently route handlers
    must do this themselves.
    *hostName* would be 'server.host.com'
    *hostAddr* would be 'server.host.com:8080'  (for the first example)

    """
    def __init__(self, pageParmsList=None, parsePost=True,
            textPlainPost=False,splitDash=True):
        ''' pageParms is a list of the page name and then paramters names for the page
        if parseParms is None, then it is assumed there are no parameters and pagename
        is extracted from the URL (using all of the URL following the site.

        e.g 'News/date/story'  for a page called 'News' with two parameters.

        if 'parsePost' is true then post data will be parsed as json data
        '''
        self.request=request
        self.saltQuery=request.query_string
        self.getData= combiParse(self.saltQuery,errors=False)
        #print('qs',self.saltQuery,self.getData)

        self.postDataRaw=request.body.getvalue().decode("utf-8")
        #print('rawpost',self.postDataRaw)

        if parsePost:
            if textPlainPost:
                self.postData= textPlainParse(self.postDataRaw)
            else:
                self.postData= combiParse(self.postDataRaw,errors=False,splitDash=splitDash)



        host= re.sub(r'^.*://','',request.url)+'/'
        self.hostName = re.match(r'(.*?)[:/]',host).group(1)
        self.hostname = self.hostName #deprecate this, inconsistent name
        self.hostAddr = re.match(r'(.*?)[/]',host).group(1)

        url=re.sub('^.*://','',request.url) #strip prefix
        #self.saltScript = re.match(r'.*/(.*)',url).group(1) #any use any more? includes extn

        #strip hostname
        self.urlInSiteFull = url = re.match(r'.*?/(.*)',url).group(1) #this time full path
        if self.urlInSiteFull.endswith('/'):
            self.urlInSiteFull=self.urlInSiteFull[:-1]
        self.setPageParms(pageParmsList)
        self.sentHeader = None

    def setPageParms(self,pageParmsList):
        """ sets self.pageParms and self.urlInSite and can adjust saltScript
        pageParmsList can be None, a string or a list
        the string is converted to a list by spitting on ','
        If pageParmsList is None, then saltscript is checked for numbic,
        in which case it is taken as a numeric 'pageParm' and the script is
        adjusted to the prior entry in the url.
        the 'pageName', the first entry in the pageParmsList is looked for in
        the full, and subsequent entries are take as pageParms.
        e.g.  'Members/Cards/1/test', with a 'pageParmsList of ['Cards,'num',other]
        would become a url of 'Members/Cards', a script of 'Cards' and a
        pageParms of ({'num':'1','other':'test'})
        """
        self.pageParms= ODict()
        if isinstance(pageParmsList,str):
            pageParmsList=pageParmsList.split(',')

        self.saltScript=  re.match(r'(?:.*/)*(.*)',self.urlInSiteFull).group(1)

        if not pageParmsList and self.saltScript.isnumeric():
            self.saltScript = re.match(
                    r'(?:.*/)*(.*)/.*',self.urlInSiteFull).group(1)
            pageParmsList=[self.saltScript,'index']

        if not pageParmsList:
            self.urlInSite = self.urlInSiteFull
        else:
            urls=self.urlInSiteFull.split('/')
            for i,u in enumerate(urls):
                if u == pageParmsList[0]:
                    break
            else:
                raise IndexError('cant find page in url')
            self.urlInSite = '/'.join(urls[:i+1])
            for j,param in enumerate(pageParmsList[1:]):
                self.pageParms[param] = None if i+j+1 >= len(urls
                    ) else urls[i+j+1]

    def setContentType(self,ctype=None):
        print('set content called',ctype)
        self.page=''

    def sendHeader(self):
        print('call to sendheader...not clear if we ever need anymore?')


    def write(self,string):
        """ we do not write to page anymore -so sending to console"""
        print('Write:', string)
        self.page+=string

def trail_filter(config):
    ''' this is a filter for the end of a route to match
    with or without a trailing slash '''
    print('tfilt:',config)
    regexp = r'([/]$|$)'

    def to_python(match):
        return match

    def to_url(value):
        return value
    return regexp, to_python, to_url


def fileExt_filter(parms):
    ''' This filter allows for file names with extensions.
    for example  <f:fileExt:file.txt.md>  will match both 'file.txt' and 'file.md'
    adding a trailing '.' <f:fileExt:file.txt.md> will also match 'file.' and 'file'
    using without extentions, eg <f:fileExt:file>
    -  will match with and without any file extentions'''
    assert parms,'fileext filter needs a paramater string after second :'
    plist= parms.split('.')
    filen=plist[0].replace(',','|')
    trail= '|' if '' in plist else ''
    exts = '|'.join( ['[.]'+p for p in plist[1:]]
           ) if not '*' in plist else '([.][^/<]*)?'
    regexp = '({})({}{})'.format(filen,exts,trail)

    def to_python(match):
        return match

    def to_url(value):
        return value

    return regexp, to_python, to_url


def deprec_staticPage(thepage,pageObj=None):
    """ page from mako but with no data prep required """
    req=ExtReq()
    bottle.TEMPLATE_PATH = paths(req.hostName)['makoPath']
    if not pageObj:
        pageObj=HtmlPage(req,None)
    pageObj.predraw()
    print('tempt d',pageObj.templateData)
    return template(thepage,name='',**pageObj.templateData)
#renderPage=staticPage
