# $Id: basicPage.py 44 2008-12-02 06:49:20Z ian $

# top level template

import os
#from lib.libfuncs import PageObject,debecho,eTreeFromXML,saltInt
#from lib.libModules import SaltTime
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import TopLevelLookupException
#import lib.sets as connections

from objdict import ObjDict
from ..mbextend import paths
import bottle
from bottle import mako_template as template
from .. import mako_templates_folder

#from saltSqlaDB import session

class PageObject:
    pass
class BasicPage(PageObject):
    """ the page for displaying the response- a special type of page! """

    @property
    def pagePath(self):  #name should change to 'pagePath' to avoid confusion

        page = self.templateData.get('pagePath','not yet rendered')
        return page if page =='/' else '/' + page
        self.thisPage = script  #script has to be passed in bottle due to clever urls!
        if self.thisPage[:1] != '/':
            self.thisPage = '/' + self.thisPage
    #thisPage=pagePath

    def __init__(self, req,view=None):

        bottle.TEMPLATE_PATH = (paths(req.hostName)['makoPath']
            + mako_templates_folder.__path__)
        # this should move to mbextend and be done once on module load!(io 2016-oct)
        #---can erase if using TemplateLookup? ...this is the active one!

        self.req = req
        self.view=view


        # debecho("basicpage : req.postData: ", req.postData)
        self.xmlMap = None
        #2015 --libinit(req)
        self.templateData = {}
        self.template = self.hostInfo('fname').split('.')[0] + '.html'#.replace('.py','.html')
        #if self.template=='/.html':
        #   self.template=="/index.html"
        path = self.hostInfo('path')

        self.paths = paths(path)
        allpaths=self.paths['makoPath']+mako_templates_folder.__path__
        lookParms = dict(directories=allpaths)
        if 'mmods' in self.paths:
            lookParms['module_directory'] = self.paths['mmods']
        #self.makoLookup = TemplateLookup(**lookParms)
        #---this is this the unused!...right now anyway

        #debecho('templateInfo', self.hostInfo('fname'), self.makoLookup) #.has_template())

        #DEPREC thost,tuser,tpass,tdb=sets.get(0)
        #need to get db parms from outside tree
        if False: #'useDB' in dir(self):# being deprecated...getcursors does this on demand and page cursor too simple
            try:
                self.db = site.getDB(path)
            except ValueError:
                self.db = None #connections.getConnection(None)
            # DEPREC  MySQLdb.connect(host=thost, user=tuser, passwd=tpass, db=tdb)
            self.cursor = self.db.cursor()
        self.saltID = None

        self.cursors = {}
        self._dbs = {} # So we can close them in __del__
        try:
            if not req._content_type_set: #pages overriding should set before this __init__
                req.content_type = "text/html"
        except AttributeError:
            req.setContentType() # must be on saltReq
        #self.sentHeader=False
        #debecho('basep',self.template)
        return

    #the following are the components of a complete url request broken into components
    @property
    def postData(self):
        return self.req.postData

    @property
    def getData(self):
        return self.req.getData

    @property
    def pageParms(self ):
        return self.req.pageParms

    def buildURL(self,pageParms=True, page=True,
                     gets=False, domain=False, pagePrefix='/'):
        """ build a URL from the component parts
            each part can be give as:
            True: include from component in page
            False: omit this component
            other: use 'other' as value for this component
            (replaces fixUrlGets)
        """

        url=pagePrefix
        if page is not False:
            url += self.req.urlInSite if page is True else page

        if pageParms is not False:
            pagebld = pageParms if not pageParms is True else self.pageParms
            if not url.endswith('/'):
                url+= '/'
            url+= '/'.join(pagebld.values())

        if gets is not False:
            getbld = gets if not gets is True else self.getData

            url += '?' + '&'.join([
                '='.join() for i in getbld.items()

            ])

        return url

    def debecho(self,*args ):
        if 'du' in self.getData:
            print(*args)


    def templateFile(self, file):
        try:
            return self.makoLookup.get_template(file)
        except TopLevelLookupException:
            #debecho('except file', file)
            return self.makoLookup.get_template(file.replace('.html', '/index.html'))

    def render(self,thispage,templatePath,**kwargs):
        self.templateData.update(kwargs)
        self.templateData['page']=self
        self.templateData['pagePath'] = templatePath
        self.templateData['thispage'] = thispage
        self.templateData['view']=self.view
        self.templateData['fields'] = (
            ObjDict() if self.view is None else self.view.fields_)
        #print('templatedat keys',self.templateData.keys())
        return template(templatePath,name='',**self.templateData)

    def applyPostData(self):
        #with view
            for key,data in self.postData.items():
                if key.startswith('field'):
                    key = key[len('field'):]
                    if key in self.view.fields_:
                        if key == 'namexType':
                            import pdb; pdb.set_trace()
                        self.view.fields_[key].value= data
                        #form data is in string format
                        #self.view.fields_[key].strvalue= data


#############################################################################################
#############################################################################################
#all below here under consideration to be deprecated

    # to be deprecated with bottle version???
    def renderFile(self, file, **kwargs):
        tmplate = self.makoLookup.get_template(file)
        echo("tmplate", tmplate)
        return tmplate.render(**kwargs)

    def setSession(self, sesDat):
        #decode session vars
        self.session = {}
        for ses in sesDat.split('-'):
            sesp = ses.split('.')
            try:
                self.session[sesp[0]] = sesp[1]
            except IndexError:
                debecho('sess elt index error', sesp)
        return


    def getCursor(self, dbid):
        try:
            return self.cursors[dbid]
        except KeyError:
            import nosync.dbsets as dbsets
            try:
                thost, tuser, tpass, tdb = dbsets.get(dbid)
            except ValueError:
                cursor=None #connections.getConnection(dbid).cursor()
            else:
                import MySQLdb
                #need to get db parms from outside tree
                print('hoist etc',thost,tuser,tpass,tdb)
                db = MySQLdb.connect(host=thost, user=tuser, passwd=tpass, db=tdb)
                self._dbs[dbid] = db
                cursor = db.cursor()
            self.cursors[dbid] = cursor
        return cursor

    def deprec_predraw(self, **extras):
        self.templateData['page'] = self
        #if 'guff' in dir(self):
        try:
            self.templateData['guff'] = self.guff
        except AttributeError:
            pass #there may be no attribute 'guff' in self
        self.templateData.update(extras)
        return
    def deprec_draw(self, **extras):
        self.predraw(**extras)
        self.write(self.templateFile(self.template).render(**self.templateData))
        return

    def deprec_write(self, strng):
        """write string to page"""
        try:
            snt = self.req.sentHeader
        except AttributeError:
            snt = False
        if not snt:
            self.req.sendHeader() #_http_header()
            #self.req.sentHeader=True
        self.req.write(strng)
        return

    def hostInfo(self, mode):
        #debecho('hi i ',dir(self.req))
        try:
            host, pagename = self.req.hostName, self.req.saltScript#self.req.uri
            #debecho('hostinf', host, pagename)
        except AttributeError:
            raise
            debecho('running old uri')
            host, pagename = self.req.hostName, self.req.uri  #still need the old one for transition

        #-host=$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF'];
        #//print "host $host dn<br>";
        #//dumpit($_SERVER,"serv");
        if mode == 'path': return host
        if mode == 'fname':return pagename#-    case "fname": return substr($host,$len+1);
        return host

    def deprec_fixUrlGets(self, gets={}, fxpage=None, pageName=''):
        """
        this is now also deprecated...moved to 'buildUrl' in this class

        this def returns the desired page (default current) with get paramters appended
        being moved from 'fmPage'...
        gets is a dict of new gets to apply
        fxpage is the full URL of the page - pageName is within same folder as current, when no fxpage supplied
        this can be used even without gets to retrieve URLs
        """
        def namesubst(fullname, pageName):
            if not pageName:return fullname
            return os.path.join(os.path.split(fullname)[0], pageName + '.html')
        """ (n) n is target number. returns url of this page with l= get parameter adjusted to n"""


        return self.req.urlInSite

        #2015- old code
        getparms = ""
        gots = []
        #for k, d in self.getData.items(): changed from dec 2015 by io
        for k,d in self.view.fields.items():
            if k in gets.keys():
                #debecho('urlg',k,d,gets[k])
                if gets[k] != None:
                    getparms += k + "=" + str(gets[k]) + "&"
                gots.append(k)
            elif k:
                getparms += k + "=" + d.get() + "&"
        if fxpage == None:
            fxpage = namesubst(self.thisPage, pageName)
        if True:#getparms :
            fxpage += "?" + getparms
        #else:
        #   fxpage+="?l="+str(n)
        for k, d in gets.items():
            if not k in gots and d != None:
                fxpage += k + '=' + str(d) + '&'
        #debecho('thispage',self.thisPage,fxpage,pageName)
        return fxpage

    def getMap(self, theFileName):
        scripts=self.paths.get('scripts',['.'])
        mapfile = open(os.path.join(scripts[0], theFileName))
        themap = []
        for mapline in mapfile:
            while mapline[ - 1] in ['/n', ' ']:
                del mapline[ - 1]
            if mapline:
                themap.append([parse(elt) for elt in mapline.split('|')])
        # now trace the current path (breadcrumbs) and note siblings
        #debecho('mp2',self.req.subprocess_env['SCRIPT_NAME']) #,str(self.req.document_root))
        thisOne = self.req.saltScript.split('/')
        #thisOne=self.req.subprocess_env['SCRIPT_NAME'].split('/')
        # really only have to find the names....paths self explanatory?
        pth = '/'
        crumbs = [themap[0]]
        thisDir = themap[0]
        for elt in thisOne[: - 1]:
            pth = os.path.join(pth, elt)
            for amap in themap:
                #debecho('buildcrumbs',amap,pth,elt)
                if pth == amap[0]['path']:
                    crumbs.append(amap)
                    thisDir = amap
                    break
        return themap, crumbs, thisDir

    def linkLists(self, crumbs, thisDir):
        """deprecate this one"""
        #debecho('crumbs',crumbs,thisDir)
        crumblist = [crumb[0] for crumb in crumbs[1:]] #should discover why first is dup
        siblist = thisDir[1:]
        return crumblist, siblist #'link1','link2'

    def linkCrumbLists(self, crumbs, thisDir):
        """ format crumbs and sibs in to lists"""
        #debecho('crumbs',crumbs,thisDir)
        crumblist = [crumb['attrs'] for crumb in crumbs[: - 1]] #last is this page!
        siblist = [child['attrs'] for child in thisDir]
        return crumblist, siblist #'link1','link2'

    def mapName(self, mapentry):
        """extract name from map - decode : parts!"""
        #print('mapname',mapentry)
        #print('mapn',mapentry['name'].split(':')[ - 1])
        return mapentry['name'].split(':')[ - 1]

    def mapURL(self, mapentry):
        #print('in mapUrl',mapentry)
        try:
            crumbs = self.crumbs
        except AttributeError:
            self.getMapCrumbs()
            crumbs = self.crumbs
        #debecho('owngets',crumbs[-1],crumbs[-1]['attrs']['gets'])
        #print('crumbs',crumbs)
        try:
            owngets = crumbs[ - 1]['attrs']['gets']
            #print('owngets',owngets)
            path = mapentry['path']
            if not '.' in path.split('/')[ - 1]:
                if path.split('/')[ - 1]:
                    #doesnt end in slash and is a dir
                    path += '/'
            getvals = dict(l=None)
            """if 'gets' in mapentry:
                gets=mapentry['gets'].split('-')
                for get in gets:
                    try:
                        getvals[get]=getattr(self,get)
                    except AttributeError:
                        pass"""
            if owngets:
                ogets = owngets.split('-')
                getvals[ogets[0]] = defVal(self.getData, 'l') #
                #debecho('getvals',getvals)
            path = self.fixUrlGets(getvals, path)

            if mapentry['path'].split('/')[ - 1].split('.')[0] == 'login' or(
                'login' in [n.lower() for n in mapentry['name'].split(':')]):
                #on a login page-make link secure
                #debecho('mapentry',mapentry,path)
                if 'nosec' in self.getData:
                    path='http://'+(self.hostInfo('path').replace('www.',''))+  path
                else:
                    path = 'https://' + (self.hostInfo('path').replace('www.', '')) +   path
                #debecho('mapentry2',path,[n.lower() for n in mapentry['name'].split(':')])
        except :
            #print('had error',mapentry['name'])
            path='not found'
        return path#mapentry['path']+"?up=33"

    def deprec_getFile(self, fname, ftype='txt'):
        """retrieves data file from dir scripts tree"""
        scripts=self.paths.get('scripts',['.'])
        thefile = open(os.path.join(scripts[0], fname))
        debecho('getfile', os.path.join(self.paths['np'][0], fname))
        res = ''
        for line in thefile:
            res += line
        if ftype == 'XML':
            return eTreeFromXML(res)
        return res

    def deprec_getXmlMap(self):
        if not self.xmlMap:
            self.xmlMap = self.getFile('sitemap.xml', 'XML')
        #debecho('xmlMap',self.xmlMap)
        return self.xmlMap

    def huntPageName(self, pageName):
        """may be able to contain the main logic for getMapCrumbs"""
        def lookIn(lookDir):
            for amap in lookDir:
                #debecho('buildcrumbs',amap['attrs'],pth,elt)
                if elt.split('.')[0] == amap['attrs']['key'].split('.')[0]:
                #if pth==amap['attrs']['path']:
                    #debecho('foundh',elt,pth)
                    return True, amap
            for amap in lookDir:
                if amap['children']:#if no children, we are at the end
                        res, bmap = lookIn(amap['children'])
                        if res:
                            return res, bmap
            return False, None


        self.getXmlMap()
        target = pageName.split('/')
        themap = self.xmlMap['children'][0]
        pth = '/'
        crumbs = [themap]
        thisDir = themap['children']
        debecho('hunt1', target)
        foundTarget = False
        for elt in target:
            pth = os.path.join(pth, elt)
            found, node = lookIn(thisDir)
            if found:#case not found in search- so now move to searching each folder
                debecho('found', pth, elt)
                foundTarget = True
                if node['children']:
                    thisDir = node['children']
                crumbs.append(node)
                #break
        #debecho('crumbs',crumbs,thisDir)
        if not foundTarget:
            thisDir = None
        debecho('hunt', [crumb['attrs'] for crumb in crumbs], thisDir)
        return crumbs, thisDir

    def getMapCrumbs(self):
        """ returns list of crumbs and siblings
        """
        return [],[] #both empty for now
        self.getXmlMap()
        thisOne = self.req.saltScript.split('/')
        #thisOne=self.req.subprocess_env['SCRIPT_NAME'].split('/')
        if thisOne and not thisOne[0]:del thisOne[0]
        # really only have to find the names....paths self explanatory?
        themap = self.xmlMap['children'][0]
        pth = '/'
        crumbs = [themap]
        thisDir = themap['children']
        #debecho('crumb1',thisOne)
        for elt in thisOne:
            pth = os.path.join(pth, elt)
            for amap in thisDir:
                #debecho('buildcrumbs',amap['attrs'],pth,elt)
                if elt == amap['attrs']['key']:
                #if pth==amap['attrs']['path']:
                    #debecho('found')
                    crumbs.append(amap)
                    if amap['children']:#if no children, we are at the end
                        thisDir = amap['children']
                    break
        #debecho('crumbs',crumbs,thisDir)
        #debecho('crumbs',[crumb['attrs'] for crumb in crumbs],thisDir)
        self.crumbs = crumbs
        self.crumbsMore = thisDir
        return crumbs, thisDir

    def saltizeName(self, name, saltWith='Salt'):
        if name.lower()[:len(saltWith)] == saltWith.lower():
            return name
        return saltWith + ': ' + name

    def ljust(self, text, sz, fillChar=''):
        """is in python - with filchar- from 2.4"""
        return str(text) + (fillChar * sz)[:sz]

    def siteLink(self, thepage, textVersion='', quote=True):
        """ will search the sitemap for either a folder with this name(and link to index)
        or an individual page ...then it will return this as a link
        if link cannot be found will return the text version in quotes
        the 'quote' parameter sets if the textVersion is text or an image link or something"""
        crumbs, folder = self.huntPageName(thepage)
        if textVersion:
            pass
        elif folder:
            textVersion = self.mapName(crumbs[ - 1]['attrs'])
        else:
            textVersion = ''
            for c in thepage:
                if c.islower():
                    textVersion += c
                else:
                    textVersion += ' ' + c.lower()
        if folder:
            link = self.mapURL(crumbs[ - 1]['attrs'])
        else:
            link = None
        return link, textVersion
    def fmtAmt(self, amt):
        """a format for amounts on the page should be set"""
        return '$%s.%02i' % (amt / 100, amt % 100)
    def match(self, text, choices, value, eltNum):
        """returns text if value matches the choiceList for current eltNumber
        the choice list has a text and a number for each elt in the list
        value can be a number (in which case it just has to match the number of a choice)
        or if value is text, it is matched against the correct text elt in the choice list
        """
        texts, nums = zip(*choices) #break choices into two lists
        if eltNum in nums: # if not we are doing something strange!
            if value in choices[list(nums).index(eltNum)]: #can match text or num!
                return str(text)
        return ''
        # eg ${page.match('selected',choices,item['value'],n)}
    def pageTitle(self):
        """ looking to extract page Title from sitemap
            should page title be in site map? ... where should it come from?
        """
        #crumbs, sibs = self.getMapCrumbs()
        return 'currently untitled' #self.mapName(crumbs[ - 1]['attrs'])

    def dispName(self, dispCol):
        return dispName(dispCol)
    #   if isinstance(dispCol,dict):
    #       return defVal(dispCol,'name','missingName')
    #   return dispCol

    def pageLead(self, row):
        """ this method is used by pages needing to send to phones
        - prefix to page and content type set
        set content type -row must contain phone data- now all commands to phone get pageLead
        """
        lead = ""
        if 'phone_id' in row:phoneid = row['phone_id']
        else: phoneid = row['id']
        if phoneid:

            if row['headers'] == 1:
                content = 'text/html'
            elif row['headers'] == 2:
                content = 'text/plain'
            else:
                content = 'text/html'
                #content='text/plain'
            self.req.setContentType(content)

            if row['htmlTags'] > 1:
                lead = "<html><body><p>"
        return lead
    def pageTrail(self, row):
        trail = ''
        try:
            phoneid = row['phone_id']
        except KeyError:
            try:
                phoneid = row['id']
            except:
                phoneid = False

        if phoneid:
            if row['htmlTags'] > 1:
                trail = "endgarb=</p></body></html>"
        return trail

class MsgPage(BasicPage):
    """docstring for MsgPage"""
    def __init__(self,req, PARMS=None):
        #prrint('pre2',req.getData)
        BasicPage.__init__(self,req)
        #prrint('par2',req.getData)

        if 'appver' in self.req.allData:
            self.appVer=self.req.allData['appver']

    def doAppVer(self,minrel='0.0,0',appSeen=None,phone=None,app='menu'):
        """ handsetapp is verion seen, minrel is what is required
         app is 'menu' or 'reg' - what is seeing the is the ver
         we then ensure ver is recorded in the db against the app that saw it
         returns 'diff status' and string version number (in tuple)
         diff= 0 (no difference- or newer)=1 first digit diff, 2= 2nd digit diff,3= minor diff
        """

        def doDiff(test,reference):
            print('dodiff',test,reference)
            compares=zip(test.split('.'),reference.split('.'))
            diff=0
            for n,comp in enumerate(compares):
                if saltInt(comp[0])>saltInt(comp[1]):
                    # test is newer !
                    break
                if saltInt(comp[0])<saltInt(comp[1]):
                    diff=n+1
                    break
            #drops out if equal
            return diff

        if appSeen==None:
            try:
                appSeen=self.appVer
            except AttributeError:
                appSeen=self.appVer=self.getData.get('appver','?.?.?')

        diff=doDiff(appSeen,minrel)
        debecho('dif',diff,appSeen,minrel)
        # now db section
        dbsets=dict(menu=dict(date='verMenuDate',time='verMenuTime',ver='verMenu')
            ,reg=dict(date='verRegDate',time='verRegTime',ver='verReg')
            )
        if phone and app in dbsets and 'id' in phone.data:
            dbset=dbsets[app]
            #debecho('diff have data and app',dbset,self.data)
            haveFlds=dbset['ver'] in phone.data
            #haveFlds=True
            #for fld,val in dbset.items():
            #   if fld not in self.data:haveFlds=False
            if haveFlds and doDiff(phone.data[dbset['ver']],appSeen): # ok we should update!!
                tdate,ttime = SaltTime.dateTime(0,["date","time"])
                debecho('doing update to ver and compare',phone.data,doDiff(phone.data[dbset['ver']],appSeen))
                phone.doUpdate(dict(id=phone.data['id'])
                    ,{dbset['date']:tdate,dbset['time']:ttime,dbset['ver']:appSeen})

        banner= diff and 'please update to new version' or ("Saltit Version %s" % appSeen)
        return diff,banner

def index(req):
    #seems this should be deprecated 2016-jan io
    #global thereq=req
    page = BasicPage(req)
    titleBar = "Salt Mobile"
    titleHead = ""
    localStyles = """
<style type="text/css">
.styleIndexText {
    color: #666666;
    font-weight: bold;
    font-size: 14px;
</style>"""
    page.bp.update(sitePageData(titleBar, titleHead, localStyles))
    page.draw()#echo(page.templateFile('basePage.html').render(bp=page.bp))
    tx = Template("hello ${data}!").render(data="world")
    import sys
    return " g'daY" + str(sys.path) + tx + '<br>' + page.hostInfo('path') + repr(page.paths)
