#!/usr/bin/env python
#2.3 2009 mar
# updates for terminator and send on
#2.2 2008 feb
#  updated import of saltmemberTable
#  removed _req references


# file management routines
from lib.libfuncs import *
import urllib
import datetime
import os.path
from dataModels.saltTable import SaltTable,SaltTblRow
# import templates.withNav as withNav
from templates.withNav import NavPage

# """def setNames(cols):
#   for key,col in cols.items():
#       col.setname(key)
#   return cols"""

def doButton(id,text,function=""):
    """  id and name are same """
    if function:
        btype="button"
        bfunc="onClick=(%s)"%function
    else:
        btype="submit"
        bfunc=""

    return '<input name="{id}" type="{btype}" id="{id}" value="{text}" {bfunc}>'.format(**locals())

def doButtonInCol(idval):
    """     function doButtonInCol($idval)"""
    id=idval[0]
    val=idval[1]
    function=idval[2]

    return (' <td><div align="center">' + "\n" + doButton(id,val,function)
        + '</div></td>'+ "\n" )

def prefSuf(mainstr,prefix="",sufix="",empty=""):
    if mainstr:
        return prefix+mainstr+sufix
    return empty


# class FmPage(withNav.NavPage):
class FmPage(NavPage):
    """ enhances page with fm(file maintenance) screen stuff"""

    def __init__(self,req,view,pageSet,membView=None,prefix=None):

        # 2015- tname=self.hostInfo('fname').split('.')[0]+'.html'
        # 2015- self.template=tname #self.hostInfo('fname').replace('.py','.html').replace('.salt','.html')
        #self.template=self.hostInfo('fname').replace('.py','.html').replace('.salt','.html')

        self.pageSet=pageSet
        self.member=membView
        if membView:
            print('saltID is ',membView.id)
        self.prefix=prefix

        self.useDB=True
        self.error=""
        self.min = self.max = 1
        super().__init__(req,view)
        #
    def render(self,*args,**kargs):
        url=self.pageSet.url
        mako=self.pageSet.mako
        #print('url mko',url,mako)
        if self.prefix:
            url='/'+ self.prefix.capitalize() + '/' + url
            mako= self.prefix.lower() + '/' + mako
        #print('url mko',url,mako)
        self.showFmForm({})
        return super().render(url,mako,*args,**kargs)


    ################################################
    #now potential legacy
    def appendToUrl(self,url,elist):
        return self.fixUrlGets(elist,url)

    def deprec_2015setRowData(self):
        rows=self.table.fetchAll(**self.table.mapRowSpec()) #self.table))
        if rows:
            rowNum=saltInt(defVal(self.getData,'l',0))
            while rowNum> len(rows):rowNum-=len(rows)
            row=rows[rowNum]
        else:
            rows=[]
            row=SaltTblRow({},self.table)
        self.theRows=rows
        self.table.data=row
        return row,rows


    def dprec_2015_draw(self,*args1,**args2):
        self.setBasePageData(*args1,**args2)
        self.templateData['table']=self.table
        #if not 'row' in self.templateData:
        #   self.templateData['row']=self.table.data
        #self.guff=''
        if hasattr(self,"mainGuff"):
            self.mainGuff()
        try:
            self.templateData['guff']=self.guff
        except AttributeError:
            pass
        # withNav.NavPage.draw(self)
        NavPage.draw(self)
        return

    def gecho(self,strng):
        try:
            self.guff+=strng
        except AttributeError:
            self.guff=strng
        return


    def checkAccess(self,codes):
        """ codes can be string...looks for any in the string """
        for code in list(codes):
            if code in self.access: return True
        return False


    def deprec_fixUrlGets(self,gets={},fxpage=None,pageName=''):
        """
        being moved to 'basicPage'
        """
        def namesubst(fullname,pageName):
            if not pageName:return fullname
            return os.path.join(os.path.split(fullname)[0],pageName+'.py')
        """ (n) n is target number. returns url of this page with l= get parameter adjusted to n"""
        getparms=""
        gots=[]
        for k,d in self.getData.items():
            if k in gets.keys():
                getparms+=k+"="+str(gets[k])+"&"
                gots.append(k)
            elif k:
                getparms+=k+"="+str(d)+"&"
        if fxpage==None:fxpage=namesubst(self.thisPage,pageName)
        #debecho('thispage',self.thisPage,fxpage,pageName)
        if True:#getparms :
            fxpage+="?"+getparms
        #else:
        #   fxpage+="?l="+str(n)
        for k,d in gets.items():
            if not k in gots:fxpage+=k+'='+str(d)+'&'
        return fxpage

    #def fixL(self,n,pageName=''):
    def urlOtherItem(self,offsett):
        ''' returns the url of another item row in the same viewset.
        '''
        row=self.view.idx_+offsett
        parms=self.pageParms.copy() #use copy so do not change actual parms
        parms['index'] =str(row)
        return self.buildURL(pageParms=parms)

    def mkjlink(self,text,gets,pageName=''):
        """ text is text to display in link
            gets is set of values to change in current getstring
            pagename (if set) is target, if not set current page is used
         """
        return ('<a href="javascript:linkit(\'%s\')">%s</a> ' %(
            self.fixUrlGets(gets,pageName=pageName),text )  )

    ''' 2015--

    def sqlQuery(self,qstr):
        self.cursor.execute(qstr)
    def sqlQueryArray(self,qstr):
        return self.table.sqlQueryArray(qstr)
        #self.cursor.execute(qstr)
        #return dict([f[0] for f in self.cursor.description],self.cursor.fetchone())
    #def checkAccess(self,code):
    #   return self.session['status'].find(code)>=0

    def getFields(self): #----being deprecated!!!!
        """() use each elt extract method to get data from post
        ...or whereever it comes for this page"""
        gf={}
        for field in self.flds:
            #name,val
            if field.inTable:
                elist=field.extract(self.postData,self)
                for name,val in elist:
                    if name: gf[name]=val
        #if gf:
        debecho("gf ",repr(gf))
        gf.update(self.table.getFields(self.postData))
        debecho("gf2 ",repr(gf),self.table.renderDict)
        return gf
    --2015 '''

    def processPostPermitt(self,permitCol):
        #does the phonenum exist?
        joinIdCol=self.table.rowSpec["joinIdCol"]
        #column in join table that points to this table

        jtable=self.table.rowSpec['join'][1:]
        from dataModels.saltMemberTable import SaltMemberTable
        saltTbl=SaltMemberTable(self)
        newrow=saltTbl.getSaltFromPhone(self.postData['otherphone'],"","id")
        debecho('newrow',newrow)
        if newrow['gspResult']==0:
            #what do we change here....
            #write new storessalts .... 3 cases, new is assistant,
            mainID=self.table.data["id"]
            sstatus=""
            newsalt=newrow["id"]
            permiss=self.postData["permission"]
            if permiss=='n':
                #check jid is the fist one!!
                jrow=self.sqlQueryArray(
                    "SELECT jid FROM %s WHERE (%s='%s')AND(salt='%s')ORDER BY jid"
                    % (jtable,joinIdCol,mainID,saltID) )[0]

                self.sqlQuery(
                    "UPDATE %s SET salt = '%s' WHERE jid = %s"
                    % (jtable,newsalt,jrow['jid']))
            else:
                #jtable='storessalts'
                iflds={'salt':newsalt,joinIdCol:mainID,permitCol:permiss}
                self.table.doInsert(iflds,jtable)
                #   "INSERT INTO %s(salt,store,status ) VALUES (%s,%s,'%s')"
                #       %(jtable,newsalt,storeID,permiss) )
        else:
            self.error+=' permission grant failed- could not locate owner of number'
        return self.error
        # how did this get here???file:///home/ian/Sites-Local/SaltMobile/lib/fmElts.py
    def processPostDelSaltU(self):
        def haveUserDel():
            headStr="delsu-"
            headLen= len(headStr)
            for pkey,postElt in self.postData.items():
                #echo substr($pkey,0,$headLen),"|st <br>";
                if pkey[0:headLen]== headStr:
                    return pkey[headLen:]
            return False
        #
        delnum =haveUserDel()
        if not delnum:
            return False
        else:
            self.gecho ("User to delete is %s <br>" % delnum)
            jtable=self.table.rowSpec['join'][1:]
            self.sqlQuery("DELETE FROM %s WHERE jid =%s" % (jtable,delnum))
            # ??? storeRow= returnStore($saltID,getRecKey(),0);
        return True

    def processPostNew(self):
        self.table.makeNewOne()
    def processPostData(self):
        """returns true if there was a command so a new row can be read by caller"""
        print("std ",self.postData)
        if "IDl" in self.postData:
            #We have an update logical record- so save it before anything else (unless delete!)
            try:
                row=self.theRows[int(self.postData['IDl'])]
            except AttributeError:
                row=self.table.readRowSpec(self.postData['IDl'])
                self.table.getFields(self.postData)
                #debecho("upd<br>")
                self.error+=self.table.updateCurrent() # this doesnt work if direct load or directset
            except IndexError:
                if len(self.theRows)==0:
                    pass #there was nothing to save- must be first record
                else:
                    debecho('out of bounds save',self.postData['IDl'],len(self.theRows))
                    raise # dont save if we are out of bounds
            else:
                debecho('IDl0',[(key,row.colFromDb(key)) for key in row.keys()])
                row.getFromPostData(self.postData)
                debecho('IDl',[(key,row.colFromDb(key)) for key in row.keys()])
                debecho('IDl2',[(key,col.value) for key,col in row.columns.items()])
                self.error+=row.doUpdate()

        if "Update" in self.postData:
            pass #done really- IDl will accompany any update
            #   self.table.read() #;//$currentRow= returnCurrent($saltID,$_SESSION[SESSION_KEY],0); //show new data
            #// if new make new blank
        elif "New" in self.postData:
            #self.error=self.table.updateCurrent(theflds) #; //update current first
            self.processPostNew()
            #self.table.read()#;//returnCurrent($saltID,0,0);
        elif "Next" in self.postData:
            #self.table.updateCurrent(theflds)#; //update current first
            self.table.readRowSpec(relRec= +1)
            #//$currentRow= returnCurrent($saltID,$_SESSION[SESSION_KEY]+1,0);
        else: return False
        return True

    def deprec_navRecords(self):
        """ navLists is a sequence of tuples - (label,dothisOne) -"""

        #def  navList(self):
        #try:
        count=len(self.view.dbRows_)  #2015--theRows)
        #except AttributeError:
        #    count =self.table.recCount

        theMin=self.min #2015-- defVal(self.table.rowSpec,'min',0) -set view valies!
        maxrow=self.max

        navList= ( ('Save', count>=1)
                , ('New', maxrow > count)
                , ('Next',count>1)
                ,('Del',(count> theMin)and(theMin !=-1) )
                )
            # set min to -1 to disable del completely
        stri= '<table width="100%"  border="0" cellspacing="0" cellpadding="0"><tr>'
        #2015--nextfun="linkit('%s')" % self.fixL(saltInt(self.table.current)+1)
        nextfun = "linkit('{}')".format(self.urlOtherItem(1)) #move one forward
        navButs={'Save':("Update","Save",""),'New':('New','Make A New One',"")
                    ,'Next':('Next','Next>>',nextfun),'Del':('Delete','Delete','')
                    }
        for lbl,go in navList:
            if go: stri+=doButtonInCol(navButs[lbl])
        return stri+'<td>&nbsp;</td></tr></table>'

    def fmActionButtons(self):
        """ navLists is a sequence of tuples - (label,dothisOne) -"""

        #def  navList(self):
        #try:
        count=len(self.view.view_)  #2015--theRows)
        #except AttributeError:
        #    count =self.table.recCount

        theMin=self.min #2015-- defVal(self.table.rowSpec,'min',0) -set view valies!
        maxrow=self.max
        navList= ( ('Save', count>=1)
                , ('New', maxrow > count)
                , ('Next',count>1)
                ,('Del',(count> theMin)and(theMin !=-1) )
                )
            # set min to -1 to disable del completely
        #2015--nextfun="linkit('%s')" % self.fixL(saltInt(self.table.current)+1)
        nextfun = "linkit('{}')".format(self.urlOtherItem(1)) #move one forward
        navButs={'Save':("Update","Save",""),
                    'New':('New','Make A New One',"")
                    ,'Next':('Next','Next>>',nextfun),
                    'Del':('Delete','Delete','')
                }
        res=[]
        for lbl,go in navList:
            if go:
                #but=navButs[lbl]
                res.append(navButs[lbl])
        return res

    #
    def setSitePageData(self, *a, **kwa):
        if 'titleBar' not in kwa:
            kwa['titleBar']=self.view.view_.viewName_
        super().setSitePageData( *a, **kwa)


    def showFmForm(self,formStuff,passThru={}):
        """form stuff is a dict of data
        -  formStuff is dict( 'label', 'error' ....)
        -
        this function assumes an 'fmBody' function will do all the grunt work!
        """
        def deprec_fmFormBody(self,passThru={}):
            stri=""
            for field in self.flds:
                stri+=field.draw(self)
            return stri
        #----------------------------------

        """2015--
        try:
            self.table.data=self.theRows[saltInt(defVal(self.getData,'l','0'))]
        except IndexError:
            if self.theRows:
                self.table.data=self.theRows[0]
            else:
                self.table.data=SaltTblRow({},self.table)
            self.table.current=0
        except AttributeError:
            self.table.readRowSpec(defVal(self.getData,'l','0'))
        else:
            self.table.current=self.table.data.rowNumber

        try: #if row is defined... set it
            self.templateData['row']=self.row
        except AttributeError:
            self.templateData['row']=self.table.data
        """

        error= formStuff.get('error','')

        fmform={}
        fmform['label']=formStuff.get('label','')

        fmform['current']=self.view.idx_  #2015--self.table.current
        fmform['error']=error

        fmform['recLinks']=self.view.view_.labelsList_()  # self.dbrows)
        fmform['recCount']=len(self.view.view_)


        #fmform['recnav']=self.navRecords()
        fmform['fmActionButtons']=self.fmActionButtons()

        #was indented!!

        ''' hit for now jan2006
        flds=[]
        for field in self.flds:
                fl=field.draw(self)
                if fl:flds.append(fl)
        fmform['fields']=flds
        #to here

        if 'linkForm' in self.templateData:
            fmform['linkForm']='True'
        '''


        self.templateData['fmform']=fmform

        #self.templateData['fmform']['linkForm']='True'

        #self.endForm()
        return

    def extraLinkForm(self,rdict,idx):
        return ""
    def deprec_linkForm(self,me=0,title="",query="",handOver=False,modes={}
            ,statField='status',newMsg=''):
        def displayName(row):
            return defVal(row,"givenNames")+" "+defVal(row,"familyNames")
        def showPermitLabel(statField,modes):
            defLbl='Assistant'#'UnKnown'
            for mode in modes:
                if mode[0] in statField:
                    defLbl=mode[1]
                    return mode[1]
            return defLbl# use last in the list as default

        litLinkFormHead="""
  <p>&nbsp;</p>
  <table width="100%%"  border="2" cellspacing="2" cellpadding="2">

<tr>
      <th colspan="2" align="center"><div align="center">%s</div>
         </th>
</tr>"""
        #linkFormStr=litLinkFormHead    % title
        lf=dict(title=title)
        #loop for each permission
        #//$res = sql_query("SELECT storessalts.status
        #//                   FROM storessalts
        #//                    WHERE (store = $storeID) ");

         #//            ."  FROM storessalts,salts,phoneNumbers
         #//        WHERE (jid = $storeID)AND(salts.id=storessalts.salt)and(phoneNumbers.salt= salts.id) ");
        rows=[]
        lastjoin,theOwner,idx=0,0,0

        self.table.cursor.execute(query)
        res=self.table.cursor.fetchall()
        names=[desc[0] for desc in self.table.cursor.description]
        for jres in res:
            j=dict(zip(names,jres))
            #debecho("j",j)
            key=defVal(j,"salt")
#//      $j2 =mysql_fetch_array(sql_query("SELECT *
#//                      FROM salts
#//                       WHERE (salts.id= '$key') "));

            thisSalt= defVal(j,"salt")
            thisJoin= defVal(j,"jid")
            if theOwner==0: theOwner= thisSalt
            if lastjoin != thisJoin:#- multiple phones will make it repeat!!!
                idx+=1
                linkStatus= defVal(j,statField)
                #dumpit($linkStatus,"jj")
                button= '<input name="delsu-%s" type="submit" id="delus-%s" value="Delete" />' %(
                    thisJoin,idx)
                if (theOwner== thisSalt)and(idx ==1):
                    button="" #; //cant delete 1st instance
                uType= ( (theOwner== thisSalt and idx==1) and "Owner"
                    or showPermitLabel(linkStatus,modes))
                #linkStatus.find('C') >=0 and "Manager" or "Assistant"))
                extras=self.extraLinkForm(j,idx)
                debecho('utype',uType)
                #rows.append(dict(text=("<tr><td>%s</td><td>%s %s %s %s</td></tr>" % (
                #   displayName(j),defVal(j,"phoneNum"),uType,button,extras ))))
                rows.append(dict(name=
                   displayName(j),phoneNum=defVal(j,"phoneNum")
                   ,type=uType,button=button,xtras=extras ))

            else:
                pass #echo "<tr><td colspan=\"2\">There is one!!!<tr>";

            lastjoin=   thisJoin #// never used again!
        #end of loop
        lf['rows']=rows

        modeStr='<td><p><input name="permission" type="radio" value="%s" >%s</td></p>\n'
        setNewOwnerStr=modeStr %(
            "n",' new owner (i will no longer manage this store) ')

        allModes=""
        for mode,mname,mlongName,mhelp in modes:
            allModes+=modeStr %(mode,mlongName)
        #debecho('tho',theOwner,me);
        lf['usage']=newMsg
        lf['modes']=allModes
        lf['lastMode']=(theOwner== saltInt(me)and handOver)and setNewOwnerStr or "&nbsp;"
        self.templateData['linkForm']=lf
        #self.templateData['fmform']['linkForm']='True'
