from collections import OrderedDict as ODict
from enum import Enum

from objdict import (ObjDict)

from .viewFields import BaseField,Case,FieldItem
Section = Enum('ViewSection','all header main footer current')
# 'edit' in Case.__members__
import saltMongDB

def get_dict_attr(obj,attr):
    for obj in [obj]+obj.__class__.mro():
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    raise AttributeError

class BaseFieldDict(ODict):
    def __init__(self,*args,**kwargs ):
        super().__init__(*args,**kwargs)

    #code

class FieldDict(ODict):
    def __init__(self,view,basef,*args,**kwargs ):
        super().__init__(*args,**kwargs)
        self.view=view
        self.main=ODict()
        self.head=ODict()
        self.foot=ODict()
        cdict=self.main
        for nm,f in basef.items():
            self[nm]=cdict[nm]=FieldItem(view,f)
        self.Section=Section
        self.Case=Case


    def __2call__(self,*args,**kwargs):
        self.view.loop(*args,**kwargs)

    def __call__(self,section=Section.current,case=Case.viewAll ):
        view=self.view

        if section in (Section.all, Section.header):
            for name,field in self.head.items():
                if field.cases is None or case in field.cases:
                    yield field

        if section in (Section.all, Section.main, Section.current):
            doAll = section is not Section.current
            count = 1 if not doAll else len(view.dbRows_)
            save=view.idx_
            for i in range(count):
                view.setRow_(i,doAll)
                for name,field in self.main.items():
                    if field.cases is None or case in field.cases:
                        yield field
            view.setRow_(save,doAll)
        if section in (Section.all, Section.footer):
            for name,field in self.foot.items():
                if field.cases is None or case in field.cases:
                    yield field

    def loopRows(self):
        """ an iterator to set each row in turn as current """
        save=self.view.idx_
        for i in range(len(self.view.dbRows_)):
            self.view.idx_ = i
            yield self.view
        self.view.idx_=save

class ViewRow:
    """ this is just a concept for now, but the idea is to have a view
    consist, at least logically, of a number of view rows.
    so view[n]  is the nth row:
    .    this would allow an improved interation through a view
    .    plus allow storing references to a specific row within a view.
    each view could still have a 'default' row which can be set by
    "idx _" as happens currently

    so for example- an actual view could really be a view row
    which returns a new view row object when indexed. the new viewrow object
    would have the same data for all except _idx?  copy object, reset idx?
    would that work? would share rows and fields. what else would not be shared
    so viewObj[1] is copy of view with _idx set to 1?

    this would be neater if what was instanced was::

        view self._idx,self.underlying_view

    """
class BaseView:
    """ a view is an object model containing view specific model in addition to potentially one or more
    database row models.
    Joins views are launched with the base join table
    or directly.  if a view is instanced directly- then 'join' fields are not
    available, and access will be an error
    As properites of any name can be added and should not colide with

    A view is usually specific to one or mode data base rows, but allows for operations (such as 'next')
    to change the database row appearing in the view.
    Views can be input as well as output.
    View fields values can be retrieved and set as properties within the view, but can also be accessed from

    \_baseFields {}   class property, is an ordered dict of all 'field' properites sorted by order
    fields\_  {}      is an instance object controlling access to odict  (property,instance) pairs for accessing:
    .                    both value and properties of a field
    joins\_ []      if rows are collections built from joins,
    .                list of entries that contain the actual rows.
    .                field searches occur in order of the list
    """
    _baseFields =None

    def __init__(self,*args,**kwargs):
        self.joins_=ObjDict()
        self.dbRows_ = self.getRows_(*args,**kwargs)
        if True: # self.dbRows_:
            self.changes_=[ObjDict() for r in self.dbRows_]
            if not self._baseFields:
                #print('setfields',self.viewName_)
                self.buildBaseFields_()
            self.fields_ = FieldDict(self,self._baseFields)
        else:
            self.changes_= []
            self.fields_=ODict()
        self.idx_ = 0
    @property
    def joinkeys_(self):
        return list(self.joins_.keys())
    def getJoin_(self,collectName,findFilt):
        collect=saltMongDB.baseDB.db.get_collection(collectName)
        result=collect.find(findFilt)
        result = [ObjDict(res) for res in result]
        assert len(result)==1,'Error with find for ()join'.format(collectName)
        self.dbRows_[self.idx_][collectName]=result[0]

    def update_(self):
        for change in self.changes_:
            if change:
                if '_id' in self.dbRows_[self.idx_]:
                    update={'$set':change}
                    filter=dict(_id=self.dbRows_[self.idx_]['_id'])
                    u=self.dbRowSrc_.update_one(self.filter_,update)
                else:
                    # no _id, so should be an insert!
                    u=self.dbRowSrc_.insert(change)
                #import pdb; pdb.set_trace()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.update_()

    def buildBaseFields_(self ):
        """ called once for the class """

        fields=BaseFieldDict()
        #fields.__call__ = self.loop
        self.__class__._baseFields = fields
        #self.rows =self.getRow()
        cls=self.__class__
        holder=[]
        for thiscls in [cls] + cls.mro()[:-2]: #skip object and baseView
            for attribName in list(thiscls.__dict__):
                #if at in self.__dict#    at = getattr(cls,a)

                if isinstance(thiscls.__dict__[attribName],BaseField):
                    attribObj = thiscls.__dict__[attribName]
                    theRow = self.dbRows_[0] if self.dbRows_ else ObjDict()
                    name = attribObj.setup(attribName,theRow,self)
                    holder.append( (attribObj.instanceNum,attribName,attribObj))
        for num,key,obj in sorted(holder):
            #print('hkey',key)
            fields[key]= obj

        #need to set main,head,foot - but as properties of fields_ in the end!
        #print('hold',holder)
        #print('sholder',sorted(holder))
    def insert(self):
        """could assumes there are no other rows, and not need a  +=?
        """
        self.dbRows_+=[ObjDict()]
        self.changes_+=[ObjDict()]

    def __len__(self):
        return len(self.dbRows_)

    def loop_(self,section=Section.all,case=Case.viewAll ):

        group = [self.fields,self.head,self.main.self.foot][section]
        for field in group:
            if field.cases is None or case in field.cases:
                yield field


    def getRows_(self,args):
        """ overwrite getRows to retrieve rows from db within the view
         note: non dbase view can have no rows at all
        """
        #print('args',args[0])
        return [] if not args else args[0]

    def setRow_(self, value, condition=True):
        if condition:
            self.idx_ = value

    def labelsList_(self):
        """ list of the labelfields from dbRows
        """
        # print([ getattr(row,self.rowLabel) for row in self.dbrows])
        try:
            return [getattr(self, self.rowLabel_) for row in self.fields_.loopRows()]
        except AttributeError:
            return ['no labels' for row in self.dbRows_]

    def deprecmkList(self, rows=None, pageName=None):
        """ replacement for listTbl -expects mako to format
        handles returning whole row, but also used to give list of labels.
        this version only handles list of labels
        """
        if not rows:
            rows = self.fetchAll(**self.mapRowSpec())  # do a

        def arow(n, row):
            return n, pageName, ','.join([row[listField] for listField in self.listFields])

        return [arow(n, row) for n, row in enumerate(rows)]
