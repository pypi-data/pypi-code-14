# may 08 - preparing to deprecate
# original design had site specific data
# then basic page added to separate non-site specific
# now what is left most done by mako
#
# ver 2.2 feb 2008
# added 'page' to templateData to allow access to routines
#

# top level template
import sys
#sys.path.append("/home/saltsafe/www/lib")
#from lib.libfuncs import *
from mako.template import Template
from mako.lookup import TemplateLookup
import urllib

from .basicPage import BasicPage
#from bottle import mako_template as template
#import bottle

def echo2(str):
    global theReq
    theReq.write(str)

def defval2(arr,key,defv=''):
    if hasattr(arr,'has_key')and arr.has_key(key):
        return arr[key]
    return defv

class TrPic(object):
    def __init__(self,page):
        self.thePic=dict(pic='images/bannerRightPic.png',width=290,height=110,border=0)
        self.page=page
        return
    def set(self,pic):
        thePic={}
        thePic['pic']='images/bannerRightPic.png';
        thePic['width']='290';
        thePic['height']='110';
        thePic['border']='0';
        if pic =='images/WebCoffeeCups95.jpg':
            thePic['pic']='images/bannerRightPic.png';
            self.thePic=thePic
        elif pic=='POS':
            thePic['pic']='images/bannerRightPOS.png';
            self.thePic=thePic

        elif isinstance(pic,dict):
            thePic.update(pic)
            self.thePic=thePic
        else :
            self.thePic=pic



    def draw(self):
        if isinstance(self.thePic,dict):
            pic=self.thePic
            url=self.page.staticPrefix+'/'+pic['pic']
            return('<img src="%(url)s" width="%(w)s" height="%(h)s" border="%(b)s">' %
            dict(url=url,w=pic['width'],h=pic['height'],b=pic['border']) )
        else:
            return self.thePic
        return
class SitePage(BasicPage):

    def __init__(self,req,view=None):


        super().__init__(req,view)


        page=req.saltScript
        #page= req.subprocess_env['REQUEST_URI'].split('?')[0]

        slashcount=page.count("/")
        staticPrefix="/html"
        if(page.count("/n/")):
           slashcount-=1 # needed on the 'n' server
        while(slashcount >1):
            slashcount-=1
            staticPrefix+="/.."
        self.staticPrefix=staticPrefix
        #ok - did it!
        self.topRightPic=''

        return


    def sendHeader(self):
        #if not self.sentHeader:
        self.req.sendHeader() #send_http_header()
        #self.sentHeader=True
        return
    def echo2(self,str):
        #global theReq
        self.sendHeader()
        self.req.write(str)
    """def templateFile(self,file):
        return self.makoLookup.get_template(file)
    def renderFile(self,file,**kwargs):
        tmplate= self.makoLookup.get_template(file)
        echo("tmplate",tmplate)
        return tmplate.render(**kwargs)
    """

    def theHeader(self):
        #global titleBar,localStyles,staticPrefix
        return dict(title=self.titleBar,localStyles=self.localStyles,staticPrefix=self.staticPrefix)
    def outerBody(self):
        return {}
    def bannerRow(self):
        #topRightPic#,titleHead,staticPrefix
        #trpic=self.topRightPic
        #if hasattr(trpic,'has_key'):#is_array(trpic):
        #       trpic='<img src="'+ self.staticPrefix + '/' + defVal(trpic,'pic')+ '" width="'\
        #   + defVal(trpic,'width') + '" height="' + defVal(trpic,'height') + '"'
        return dict(trpic=TrPic(self),titleBar=self.titleBar)
    def topMenuRows(self):
        #global saltQuick,staticPrefix,SESSION
        if 0:#SESSION.has_key("saltQuick"):
            saltQuick= SESSION["saltQuick"]
            logInOut= 'Logout: ' + saltQuick
        else:
            saltQuick= '';
            logInOut= 'Login.';
        return dict(logInOut=logInOut,saltQuick=saltQuick)

    def navAndBody(self):
        return {}#global template

    def render(self,thispage,templatePath,**kwargs):
        self.setSitePageData()
        self.templateData.update(kwargs)
        return super().render(thispage,templatePath,**self.templateData)

    def setSitePageData(self,titleBar="",titleHead="",localStyles="",nav={}):
        self.titleBar=titleBar
        self.rawnav=nav
        self.appDraw={}
        self.titleHead=titleHead
        self.localStyles=localStyles
        #self.echo(" urlp "+staticPrefix+ "  ")
        bp={}
        bp.update(self.theHeader())
        bp.update(self.outerBody())
        bp.update(self.bannerRow())
        bp.update(self.topMenuRows())
        bp.update(self.navAndBody())
        self.templateData['bp']=bp
        self.templateData['site']=bp

    def setBasePageData(self,*args,**kwargs):
        self.setSitePageData(*args,**kwargs)

        #self.echo(self.templateFile('basePage.html').render(bp=self.bp))
        # #navAndBodyEnd()
        #self.theFooter()
        # now the test for the main index page
    def drawNavBar(self):
        pass
    def deprec_draw(self):
        self.guff=''
        if hasattr(self,"mainGuff"):
            self.mainGuff()
        self.templateData['guff']=self.guff
        #tobasic#  self.templateData['page']=self
        BasicPage.draw(self)
        # use base class now#self.echo(self.templateFile(self.template).render(**self.templateData))
        return

    def nowInBasicPage__hostInfo(self,mode):
        #debecho('hi i ',dir(self.req))
        #host,pagename=self.req._req.hostname,self.req.uri
        host,pagename=self.req.hostname,self.req.uri
        #debecho('hostinfo',host,pagename)
        #-host=$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF'];
        #//print "host $host dn<br>";
        #//dumpit($_SERVER,"serv");
        if mode=='path': return host
        if mode=='fname':return pagename#-  case "fname": return substr($host,$len+1);
        return host


    def deprec2015_getcooks(self,inSession): #not with bottle
        """if not hasattr(self,'cooks'):
            #debecho('req',dir(self.req))
            if hasattr(self.req,'headers_in'):
                #debecho('req head',self.req.headers_in)
                rawcooks = defVal(self.req.headers_in, "Cookie" ,"")
            else: rawcooks=''
            #getline=self.req._req.subprocess_env["QUERY_STRING"]
            #hostname=self.req._req.hostname
            getline=self.req.subprocess_env["QUERY_STRING"]
            hostname=self.req.hostname
            safesplit=lambda x,y: len(x.split(y)) ==2 and x.split(y) or [x.split(y)[0],""]
            self.getData=(dict([safesplit(elt,'=') for elt in getline.split('&')]))
            #   getData=dict(zip(["=".split(elt) for elt in "&".split(getline)]))
            self.getDataline=getline
            " ""echo("dbg" +repr(dir(self.req)))
            debecho("\n<br>getData " +repr(self.getData))
            debecho("\n<br>dbg2 uri" +repr((self.req._req.uri)))
            debecho("\n<br>dbg2 fname" +repr((self.req._req.filename)))" ""
            debecho("\n<br>dbg2 subpr", hostname)#(self.req._req.subprocess_env))
            " ""debecho("\n<br>dbg2 read" +repr((self.req.headers_in)))
            debecho("\n<br>dbg2 read" +repr((self.req._req.read())))" ""
            #self.thisPage=self.req._req.uri
            self.thisPage=self.req.uri
            self.cooks={}
            self.session={}
            debecho('rawcook',rawcooks,inSession)
            for ck in rawcooks.split('; '):
                if ck and '=' in ck:
                    cks=ck.split("=")
                    if cks[0]=='sess':
                        #decode session vars
                        for ses in cks[1].split('-'):
                            sesp=ses.split('.')
                            try:
                                self.session[sesp[0]]=sesp[1]
                            except IndexError:
                                debecho('sess elt index error',sesp)
                        debecho('session from cooks',self.session)
                    else:
                        self.cooks[cks[0]]=cks[1]
            self.saltID=-1 #allow other constructors to proceed
        --->>> all in basicPage"""
        BasicPage.getCooks(self)
        # now the enhanced!
        hostname=self.req.hostname
        if inSession and "PHPSESSID" in self.cooks and self.session=={}:
            f = urllib.urlopen("http://%s/sess.php?sess=%s" %
              (hostname,self.cooks['PHPSESSID']) )
            debecho('f=',"http://%s/sess.php?sess=%s" %
              (hostname,self.cooks['PHPSESSID']) )
            a=f.read()
            for ck in a.split('&'):#f.read().split('&'):
                #debecho('chook raffle',ck,a)
                cks=ck.split('=')
                if len(cks)>1:
                    self.session[cks[0]]=cks[1]
                else: pass#print 'err ck',ck
        if "saltID" in self.session :
        #//in session--- do global check?
            debecho('sess',self.session)
            self.saltUser = defVal(self.session,"saltUser")
            self.saltID = self.session["saltID"]
            self.access= defVal(self.session,"access")
            self.quickName= defVal(self.session,"saltQuick")
            if 'helpDesk' in self.getData:
                from dataModels.saltMemberTable import SaltMemberTable
                sTable=SaltMemberTable(self)
                data=sTable.getSaltFromPhone(self.getData['helpDesk'],None)
                debecho('data imp',data)
                self.saltID=data['id']#self.getData['impersonate']

                #self.quickName= defVal(self.session,"saltQuick")
                #self.saltID=self.getData['impersonate']
        return
    #getCooks=getcooks

def index(req):
    #global thereq=req
    page=BasePage(req)
    titleBar="Salt Mobile Home Page"
    titleHead=""
    localStyles ="""
<style type="text/css">
.styleIndexText {
    color: #666666;
    font-weight: bold;
    font-size: 14px;
</style>"""
    page.setBasePageData(titleBar,titleHead,localStyles)
    page.draw()#echo(page.templateFile('basePage.html').render(bp=page.bp))
    tx= Template("hello ${data}!").render(data="world")
    import sys
    return " g'daY"+str(sys.path) + tx + '<br>'+page.hostInfo('path')+repr(page.paths)
