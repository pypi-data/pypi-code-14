#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from old_code.populateNewsletterDB import new
import datetime
import inspect
import logging as logging
import pickle
import threading
import weakref

from estoolbox import dbNow, dateToMysqlStr, dateTimeToMysqlStr, isEqual
from future.utils import with_metaclass

__author__ = 'Marco Bartel'

LOG = logging.getLogger(__name__)

def setModelPath(path=""):
    DbSingletonClass.modelPath = path

class DbModelRelation(object):
    """
    Basisklasse einer Tabellen-Relation. Sie stellt innerhalb eines DbModels
    eine Relation zu einem anderen DbModel dar. Die Definition erfolgt innerhalb
    des DbModels muss im filter ein oder mehrere vorhanden Felder referenzieren.
    Dadurch wird es zur Laufzeit möglich dynamisch auf die Objekte der in der Relation
    befindlichen Tabelle zuzugreifen

    Beispieldefinition:
        CART_ID = DbModelField("", int, 0)
        CART = DbModelOneToOneRelation(singletonClass=Cart, filter={"ID": CART_ID})

    """

    def __init__(self, singletonClass=None, filter={}, newObjectIfNotFound=False):
        self.singletonClassName = singletonClass
        self.singletonClass = None
        self.filter = filter
        self.newObjectIfNotFound = newObjectIfNotFound

    def transformFilter(self, obj):
        """
        Generiert ein Filter-Dictionary welches auf Basis des am Objekt definierten
        filter (self.filter) die DbModelFields mit den am übergebenen Objekt
        anliegenden Feldinhalten ersetzt.

        :param obj:
        :return: dict Filter-Dictionary mit ersetztem Inhalt
        """

        generatedFilter = {}
        for name, value in self.filter.items():
            if isinstance(value, DbModelField):
                # name im filter ist ein feld, dann den wert des feldes am object
                # zum suchen verwenden.
                # feld am objekt ermitteln
                for fieldName, field, in obj.dbModel.modelFields().items():
                    if field == value:
                        break
                value = getattr(obj, fieldName)
            generatedFilter[name] = value
        return generatedFilter

    def getRelationData(self, obj):
        """
        Liefert dynamisch die Daten aus dem in der Relation definierten Model.
        Bei One-To-One ein einzelnes Objekt, bei mehreren Objekten eine Liste von Objekten

        :param obj:
        :return: DbSingletonClass oder list mit DbSingletonClass-Instanzen
        """
        return None

    def relatedModel(self):
        return DbSingletonClass.getChildClasses()[self.singletonClassName].dbModel


class DbModel(object):
    """
    Basisklasse eines Db Datenbank Models
    """
    cachedModelFields = None
    cachedModelRelations = None
    cachedPrimaryKey = None
    singletonClass = None

    @classmethod
    def modelFields(cls):
        """
        Liefert ein Dictionary mit allen im Model definierten DbModelFields.

        :return: dict Dictionary mit FeldName:FeldObjekt Paaren
        """
        if cls.cachedModelFields is None:
            cls.cachedModelFields = {}
            for key in dir(cls):
                if key[0] != "_":
                    if not key.startswith("cached"):
                        attr = getattr(cls, key)
                        if isinstance(attr, DbModelField):
                            cls.cachedModelFields[key] = attr

        return cls.cachedModelFields

    @classmethod
    def modelRelations(cls):
        if cls.cachedModelRelations is None:
            cls.cachedModelRelations = {}
            for key in dir(cls):
                if key[0] != "_":
                    if not key.startswith("cached"):
                        attr = getattr(cls, key)
                        if isinstance(attr, DbModelRelation):
                            cls.cachedModelRelations[key] = attr
        return cls.cachedModelRelations

    @classmethod
    def primaryKey(cls):
        """
        Liefert den PrimaryKey des Models
        :return: DbModelKey
        """
        if cls.cachedPrimaryKey is None:
            for key in dir(cls):
                if key[0] != "_":
                    if not key.startswith("cached"):
                        attr = getattr(cls, key)
                        if isinstance(attr, DbModelKey):
                            if attr.isPrimaryKey():
                                cls.cachedPrimaryKey = attr
        return cls.cachedPrimaryKey

    @classmethod
    def primaryKeyName(cls):
        """
        Liefert den Namen des PrimaryKeys des Models
        :return: DbModelKey
        """
        for key in dir(cls):
            if not key.startswith("_"):
                if not key.startswith("cached"):
                    attr = getattr(cls, key)
                    if isinstance(attr, DbModelKey):
                        if attr.isPrimaryKey():
                            return key

    @classmethod
    def getQueryWhereFromPrimaryKey(cls, **kwargs):
        modelfields = cls.modelFields()

        primaryKeyFields = cls.primaryKey().fields()
        primaryKeyData = {}
        for fieldName, value in kwargs.items():
            if fieldName in primaryKeyFields.keys():
                primaryKeyData[fieldName] = fieldName + "=" + primaryKeyFields[fieldName].convertForSQL(value)

        if len(primaryKeyData) == len(primaryKeyFields):
            where = " and ".join(primaryKeyData.values())
            return where

    @classmethod
    def parseFilter(cls, filter={}):
        modelFields = cls.modelFields()
        for key, value in filter.items():
            if not isinstance(value, DbFilter):
                filter[key] = "=" + modelFields[key].convertForSQL(value)
        return filter

    @classmethod
    def getQuerySQL(cls, primaryKeyValues):
        """
        Generiert ein SQL-Select-Statement zur Abfrage eines Datensatzes unter Angabe des
        Primärschlüssel-Wertes

        :param kwargs: Felder des PrimaryKeys
        :return: str SQL-Select-Statement
        """
        modelfields = cls.modelFields()

        where = cls.primaryKey().getWhereStatement(primaryKeyValues)
        if where != "":
            msql = "select %s from %s where %s" % (
                ",".join(modelfields.keys()),
                cls.dbTableName,
                where
            )
            return msql
        else:
            return ""

    @classmethod
    def getInsertSQL(cls, dataDict={}):
        for fieldName, fieldValue in dataDict.items():
            dataDict[fieldName] = cls.modelFields()[fieldName].convertForSQL(fieldValue)

        insertQuery = "insert into %s(%s) values(%s)" % (
            cls.dbTableName,
            ",".join(dataDict.keys()),
            ",".join(dataDict.values())
        )
        return insertQuery

    @classmethod
    def modelMatchingFields(cls, dbModel, withPrimaryKeys):
        ownFields = cls.modelFields().keys()
        if not withPrimaryKeys:
            ownFields = list(set(ownFields) - set(cls.primaryKey().fields().keys()))
        foreignFields = dbModel.modelFields().keys()
        matchedFields = list(set(ownFields) & set(foreignFields))
        return matchedFields

    @classmethod
    def modelHasMatchingFields(cls, dbModel, withPrimaryKeys=True):
        matchedFields = cls.modelMatchingFields(dbModel, withPrimaryKeys)
        if len(matchedFields) != 0:
            return True
        else:
            return False

    @classmethod
    def hasRelationTo(cls, dbModel):
        mrs = cls.modelRelations()
        if len(mrs) != 0:
            for mrName, mr in mrs.items():
                mrModel = mr.relatedModel()
                if mrModel == dbModel:
                    return True
        return False

    @classmethod
    def getRelationTo(cls, dbModel):
        mrs = cls.modelRelations()
        if len(mrs) != 0:
            for mrName, mr in mrs.items():
                mrModel = mr.relatedModel()
                if mrModel == dbModel:
                    return mr
        return None

    @classmethod
    def getModelFieldNameByField(cls, searchedField):
        for fieldName, field in cls.modelFields().items():
            if field == searchedField:
                return fieldName
        return None

    @classmethod
    def getJoinClause(cls, targetModel, relationName=None):
        if relationName is not None:
            relation = cls.modelRelations()[relationName]
        else:
            relation = cls.getRelationTo(targetModel)
        joinBedingungen = []

        joinClause = "join " + targetModel.dbTableName + " on "

        for fieldName, fieldValue in relation.filter.items():
            bedingung = targetModel.dbTableName + "." + fieldName + " = "
            if isinstance(fieldValue, DbModelField):
                bedingung += cls.dbTableName + "." + cls.getModelFieldNameByField(fieldValue)
            else:
                bedingung += targetModel.modelFields()[fieldName].convertForSQL(fieldValue)

            joinBedingungen.append(bedingung)

        joinClause += " and ".join(joinBedingungen)
        return joinClause


class DbModelField(object):
    """
    Basisklasse eines DbModel Datenbank-Feldes.
    """

    @staticmethod
    def SetAttributeHook(modelField):
        def realSetAttributeHook(func):
            if isinstance(modelField, list):
                modelFields = modelField
            else:
                modelFields = [modelField]

            for m in modelFields:
                if isinstance(m, DbModelField):
                    m.addSetAttributeHook(func)

        return realSetAttributeHook

    @staticmethod
    def ChangeCommitHook(modelField):
        def realChangeHook(func):
            if isinstance(modelField, list):
                modelFields = modelField
            else:
                modelFields = [modelField]

            for m in modelFields:
                if isinstance(m, DbModelField):
                    m.addChangeCommitHook(func)

        return realChangeHook

    def __init__(self, caption, fieldType, defaultValue, extra="", null=None, converter=None):
        """
        DbModel Datenbankfeld. Es können verschiedene Parameter des Feldes beeinflusst werden,
        sowie ein Converter für die Daten eingesetzt werden.

        :param caption: str Beschreibung des Feldes
        :param fieldType: type Datentyp des Datenbank Feldes
        :param defaultValue: mixed Default-Wert des Datenbank Feldes
        :param converter: DbModelConverter Objekt
        :param primaryKey: bool, ob dieses Feld der Primary Key ist.
        """
        super(DbModelField, self).__init__()
        self.__caption = caption
        self.__fieldType = fieldType
        self.__defaultValue = defaultValue
        self.__converter = None
        self.__extra = extra
        self.__null = null
        self.__hooks = []
        self.__attributeHooks = []

        if converter is not None:
            self.setConverter(converter)

    def addChangeCommitHook(self, hookFunction=None):
        if hookFunction not in self.__hooks:
            self.__hooks.append(hookFunction)

    def addSetAttributeHook(self, hookFunction=None):
        if hookFunction not in self.__attributeHooks:
            self.__attributeHooks.append(hookFunction)

    def processChangeCommitHooks(self, obj=None, value=None, oldValue=None):
        for hook in self.__hooks:
            value = hook(obj=obj, value=value, oldValue=oldValue)
        return value

    def processAttributeHooks(self, obj=None, value=None, oldValue=None, fieldName=None):
        for attrHook in self.__attributeHooks:
            value = attrHook(obj=obj, value=value, oldValue=oldValue, fieldName=fieldName)
        return value

    def fieldType(self):
        """
        Liefert den Datentyp des Feldes
        :return: type
        """
        return self.__fieldType

    def setConverter(self, converter):
        """
        Hiermit kann nachträglich der Converter des Feldes ausgetauscht werden.

        :param converter: DbModelConverter
        """
        self.__converter = converter

    def converter(self):
        """
        Liefert den aktuellen Converter des Feldes

        :return: DbModelConverter
        """
        return self.__converter

    def convertForSQL(self, value):
        """
        Liefert einen String eines Wertes aufbereitet für ein SQL Statement. Eventuell benötigte Quotes
        werden mit eingefuegt.
        :param value: Wert der vorbereitet werden soll
        :return: SQL vorbereiteter String der den übergebenen Wert darstellt.
        """
        if value is None:
            valueString = "Null"
        else:
            valueString = str(value)
            if self.__fieldType is str:
                valueString = "\"%s\"" % valueString.replace("\"", "\\\"")
            if self.__fieldType is str:
                valueString = u"\"%s\"" % valueString.replace("\"", "\\\"")
            if self.__fieldType is datetime.date:
                if value == dbNow:
                    valueString = "now()"
                else:
                    valueString = u"\"%s\"" % dateToMysqlStr(value)

            if self.__fieldType is datetime.datetime:
                if value == dbNow:
                    valueString = "now()"
                else:
                    valueString = u"\"%s\"" % dateTimeToMysqlStr(value)
            if self.__fieldType is float:
                try:
                    valueString = u"%.12f" % float(value)
                except:
                    exception = "%r, %r" % (value, type(value))
                    raise ConvertForSQLException(exception)

        return valueString

    def convertFromValue(self, value):
        """
        Fallback Converter von Wert nach str String

        :param value: Wert
        :return: str: Stringdarstellung des Wertes
        """
        if self.__converter is None:
            return str(value)
        else:
            return self.__converter.convertFromValue(value)

    def convertToValue(self, convertedString):
        """
        Fallback Converter von str String nach Wert

        :param convertedString: Stringdarstellung des Wertes
        :return: mixed: value
        """
        if self.__converter is None:
            return self.__fieldType(convertedString)
        else:
            return self.__converter.convertToValue(convertedString)

    def defaultValue(self):
        """
        Liefert den festgelegten Default-Wert des Feldes

        :return: mixed: Defaultwert
        """
        return self.__defaultValue

    def caption(self):
        """
        Bezeichnung des Feldes

        :return: str: Bezeichnung
        """
        return self.__caption

    def extra(self):
        """
        Extraoptionen des Feldes

        :return: str: Extras
        """
        return self.__extra


class DbModelDummyField(DbModelField):
    pass


class DbModelKey(object):
    """
    Basisklasse für Datenbank-Schlüssel. Momentan nur für Primary Keys interessant
    Die Definition erfolgt über die ModelDefinition.

    Beispieldefinition:

    .. code:: python

        dbPrimaryKey = DbModelKey(
            fields={
                "ID": ID,
            },
            primaryKey=True
        )

    """

    def __init__(self, fields={}, primaryKey=False):
        self.__fields = fields
        self.__primaryKey = primaryKey

    def fields(self):
        """
        Liefert ein Dictionary mit den zu dem Key gehörenden Feldern

        :return: dict: Feldname:Feld
        """
        return self.__fields

    def isPrimaryKey(self):
        """
        Liefert zurück ob der Key der PrimaryKey ist.

        :return: bool
        """
        return self.__primaryKey

    def getWhereStatement(self, fieldData):
        """
        Liefert die WHERE Clause zur Verwendung in einem SQL Query basierent auf
        der Key Definition und den übergebenen Daten

        :param fieldData: dict Feldname:Feldwert
        :return: str WHERE Clause
        """
        whereParts = []
        if len(fieldData) == len(self.__fields):
            if all(key in fieldData.keys() for key in self.__fields.keys()):
                for fieldName, field in self.__fields.items():
                    whereParts.append(fieldName + "=" + field.convertForSQL(fieldData[fieldName]))
        return " and ".join(whereParts)

    def getStringRepresentation(self, fieldData):
        """
        Liefert, basierend auf den übergebenen Daten, eine String Representation des Keys

        :param fieldData: dict Feldname:Feldwert
        :return: str String Representation des Keys oder
        :raise ValueError: wenn fehlerhafte Daten übergeben wurden
        """
        if len(fieldData) == len(self.__fields):
            if all(key in fieldData.keys() for key in self.__fields.keys()):
                ret = str(fieldData)
                return ret
        raise ValueError("PrimaryKey not well defined.", fieldData)

    def getRestUrlPart(self):
        pkParts = []
        for fname, f in self.fields().items():
            pkParts.append("{{{name}:{type}}}".format(name=fname, type=f.fieldType().__name__))
        return "/".join(pkParts)

    def injectPrimaryKeyValuesToRestUrl(self, url, primaryKeyValues={}):
        url = url.replace(":str", "")
        url = url.replace(":int", "")
        url = url.replace(":date", "")
        return url.format(**primaryKeyValues)

    def primaryKeyValuesFromRepresentation(self, string):
        """
        Liefert ein primaryKeyValues Dictionary auf Basis des übergebenen Strings, welcher
        im Format einer String-Representation eines Keys vorliegen muss
        :param string: String-Representation eines Keys
        :return: dict primaryKeyValues
        """
        ret = eval(string)
        return ret


class ConvertForSQLException(Exception):
    def __init__(self, msg):
        print
        msg


class DbModelValueMapping(object):
    def __init__(self, dbModel, keyField, valueField):
        self.dbModel = dbModel
        self.keyField = keyField
        self.valueField = valueField

    def __call__(self, db=None):
        selectQuery = "select %s, %s from %s" % (self.keyField, self.valueField, self.dbModel.dbTableName)
        return dict((x[0], x[1]) for x in db.dbQuery(selectQuery))


class DbModelValueCleanStringMapping(DbModelValueMapping):
    def __call__(self, db=None):
        data = super(DbModelValueCleanStringMapping, self).__call__(db)
        if type(data.values()[0]) in (str, str):
            ret = dict((key, " ".join(value.split())) for key, value in data.items())
        else:
            ret = dict((" ".join(key.split()), value) for key, value in data.items())
        return ret


class DbFilter(object):
    @staticmethod
    def parseFilter(filter={}):
        for key, value in filter.items():
            if isinstance(value, DbFilter):
                filter[key] = value.getFilterString()
        return filter

    def __init__(self, field, filterValue=None):
        self.filterValue = filterValue
        self.field = field

    def getConvertedValue(self):
        return self.field.convertForSQL(self.filterValue)


class DbFilterNot(DbFilter):
    def getFilterString(self):
        return "!= %s" % self.getConvertedValue()


class DbFilterIn(DbFilter):
    def getConvertedValue(self):
        return ",".join(list(self.field.convertForSQL(x) for x in self.filterValue))

    def getFilterString(self):
        return "in (%s)" % self.getConvertedValue()


class DbFilterNotIn(DbFilterIn):
    def getFilterString(self):
        return "not in (%s)" % self.getConvertedValue()


class DbFilterIsNull(DbFilterIn):
    def getFilterString(self):
        return "is Null"


class DbFilterIsNotNull(DbFilterIn):
    def getFilterString(self):
        return "is not Null"


class DbFilterLike(DbFilter):
    def getConvertedValue(self):
        return self.filterValue

    def getFilterString(self):
        return " like \"%%%s%%\"" % self.getConvertedValue()


class DbRecordNotFoundError(Exception):
    def __init__(self, cls=None, db=None, primaryKeyValues=None):
        super(DbRecordNotFoundError, self).__init__(
            "Record not found: %s %s" % (
                cls.__name__,
                primaryKeyValues
            )
        )
        self.cls = cls
        self.db = db
        self.primaryKeyValues = primaryKeyValues

    def createObject(self):
        obj = self.getUnboundObject()
        obj.create()
        return obj

    def getUnboundObject(self):
        obj = self.cls(db=self.db, primaryKeyValues=self.primaryKeyValues, loadFromDatabase=False)
        return obj


class DbUnboundSingletonInitError(Exception):
    def __init__(self, message):
        super(DbUnboundSingletonInitError, self).__init__(message)


class DbSingletonMetaClass(type):
    """
    Metaklasse fuer Singleton Db Objekte. Die Objekte die zurückgeliefert werden, existieren nur einmal
    im Speicher.
    """
    _instances = {}
    _restClientClasses = {}

    @staticmethod
    def getCacheClass(cls):
        cacheClass = cls.parentSingletonClass
        if cacheClass == True:
            mro = inspect.getmro(cls)
            for i in range(len(mro)):
                if mro[i] == DbSingletonClass:
                    cls.parentSingletonClass = cacheClass = mro[i - 1]
                    break

        if cacheClass is None:
            cacheClass = cls
        return cacheClass

    @classmethod
    def getObjectCount(cls):
        ret = {}
        for n, c in cls._instances.items():
            ret[n] = 0
            for s in c.values():
                ret[n] += len(s)
        return ret

    @classmethod
    def deleteClassInstance(cls, obj):
        cacheClass = cls.getCacheClass(obj.__class__)
        del cls._instances[cacheClass][id(obj.db)][obj.primaryKeyRepresentation()]

    @classmethod
    def bind(cls, obj):
        cacheClass = cls.getCacheClass(obj.__class__)
        cls._instances[cacheClass][id(obj.db)][obj.primaryKeyRepresentation()] = obj
        obj.unbound = False

    @classmethod
    def instances(cls):
        return cls._instances

    def __call__(cls, *args, **kwargs):
        """
        Konstruktor für neue Objekte. Es wird nachgesehen ob es dieses Objekt schon gibt, wenn ja wird nur eine
        Referenz zurückgeliefert, statt eine neue Instanz zu generieren.

        Klasse, Db-System und primaryKeyValues dienen dabei zur eindeutigen Identifikation. Db Objekt
        und primaryKeyValues sind Keyword Argumente.

        :param args: Argumente
        :param kwargs: Keyword Argumente. db, id muessen vorhanden sein um ein Objekt zu referenzieren
        :return: Objekt Referenz eines Singleton Objektes
        """

        # defaultwerte vorbelegen
        kw = {
            "db": None,
            "primaryKeyValues": None,
            "loadFromDatabase": True,
            "dataDict": {},
            "unbound": False
        }
        kw.update(kwargs)

        db = kw["db"]

        # suche nach parentSingletonClass falls nicht gesetzt
        # passiert nur einmalig wenn true

        cacheClass = DbSingletonMetaClass.getCacheClass(cls)

        if cacheClass not in cls._instances:
            cls._instances[cacheClass] = {}
            cls.cacheModelRelations()

        systemIdentifier = id(db)

        if systemIdentifier not in cls._instances[cacheClass]:
            cls._instances[cacheClass][systemIdentifier] = weakref.WeakValueDictionary()
            # cls._instances[cacheClass][systemIdentifier] ={}

        if kw["primaryKeyValues"] is None:
            kw["loadFromDatabase"] = False
            if cls.autoGeneratePrimaryKeyValues:
                kw["primaryKeyValues"] = cls.generatePrimaryKeyValues(db=db)
            else:
                kw["unbound"] = True

        if kw["unbound"]:
            newObj = super(DbSingletonMetaClass, cls).__call__(*args, **kw)
            if newObj.initOk:
                newObj.setAutoCommitEnabled(False)
                newObj.db = db
                return newObj
            else:
                raise DbUnboundSingletonInitError("Unbound Object konnte nicht erstellt werden.")

        else:
            primaryKeyValues = kw["primaryKeyValues"]
            primaryKeyString = cls.dbModel.primaryKey().getStringRepresentation(primaryKeyValues)

            if "loadFromDatabase" in kw:
                if not kw["loadFromDatabase"]:
                    if not "dataDict" in kw:
                        kw["dataDict"] = primaryKeyValues
                    else:
                        kw["dataDict"].update(primaryKeyValues)

                else:
                    kw["dataDict"] = cls.loadFromDatabase(db=db, primaryKeyValues=primaryKeyValues)

            # check gibts schon ein dict für diese id in dem db system
            if primaryKeyString not in cls._instances[cacheClass][systemIdentifier]:
                newObj = super(DbSingletonMetaClass, cls).__call__(*args, **kw)
                if newObj.initOk:
                    newObj.db = db
                    cls._instances[cacheClass][systemIdentifier][primaryKeyString] = newObj
                else:
                    return None
            else:
                if "dataDict" in kw:
                    # updaten der daten wenn schon vorhanden.
                    cls._instances[cacheClass][systemIdentifier][primaryKeyString].loadFromDict(kw["dataDict"])

            return cls._instances[cacheClass][systemIdentifier][primaryKeyString]


class DbBareDataClass(object):
    """
    Basis Datenklasse um Objekte statt Dictionaries zu nutzen
    um einen mehr pythonischen Weg der Datenhaltung zu implementieren
    """

    def __init__(self, dataDict=None):
        if dataDict is not None:
            self.loadFromDict(dataDict)

    def updateFromObject(self, obj):
        newObj = DbBareDataClass.loads(obj.dumps())
        for key, value in newObj.dataDict().items():
            if not hasattr(self, key):
                setattr(self, key, value)
            else:
                attr = getattr(self, key)
                if isinstance(attr, DbBareDataClass):
                    attr.updateFromObject(value)
                else:
                    setattr(self, key, value)

    def dumps(self):
        """
        Serialisiert eine DbBareDataClass Instanz zu einem String.
        DbBareDataClass Instanzen in den Daten werden ebenfalls rekursiv mit serialisiert.

        :return: String
        """
        return pickle.dumps(self)

    def prettyStr(self):

        ret = []
        data = self.dataDict()
        for key, value in data.items():
            if isinstance(value, DbBareDataClass):
                value = value.__repr__()
            else:
                # if type(value) == datetime:
                #     value = u"%s" % value.__repr__()
                #
                # elif type(value) in (str, str):
                #     value = u"'%s'" % value
                #     value = value.replace("\\", "\\\\")
                value = "{value}".format(value=value.__repr__())
            ret.append(u"'{key}': {value}".format(key=key, value=value))
        return u"DbBareDataClass(dataDict={data})".format(data=",".join(ret))

    def __repr__(self):
        return self.prettyStr()

    @classmethod
    def loads(cls, data):
        # """
        # Erstellt eine DbBareDataClass Instanz auf Basis eines vorher serialisierten Strings.
        #
        # :param data: String
        # :return: DbBareDataClass Instanz
        # """
        # data = eval(data.replace("\\", "\\\\"))
        # return cls(dataDict=data)
        return pickle.loads(data)

    def loadFromDict(self, dataDict):
        """
        Lädt die Daten eines Dictionaries und stellt diese als Objektattribute
        zur Verfügung. Die Dictionary-Keys werden die Attributnamen und die Values
        zu den Werten der Attribute.

        :param dataDict:
        """
        self.__dict__.update(dataDict)
        # for key, data in dataDict.items():
        #     setattr(self, key, data)

    def dataDict(self):
        """
        Liefert ein Dictionary der am Objekt anliegenden Attribute
        ohne Funktionen und protected Members.

        :return: dict: Attribute/Werte
        """
        ret = {}
        for key, value in self.__dict__.items():
            if key[0] != "_":
                ret[key] = value
        return ret


class DbDataClass(DbBareDataClass):
    """
    Erweitert die DbBareDataClass um die Verwendung eines
    DbModels. Wird kein Dictionary zum laden angegeben, wird
    das Objekt mit den Defaultwerten des Models befuellt.
    Ausserdem bietet diese Klasse eine ChangeDetection Funktionalität die
    eingeschaltet werden kann.
    """

    cachedModelRelationNames = []
    cachedModelRelations = None
    dbModel = None
    dbModelDefaultValues = None
    cachedModelFieldNames = None
    cachedModelFields = None
    cachedModelRelationsLock = threading.Lock()

    @classmethod
    def cacheModelRelations(cls):
        if not cls.cachedModelRelations:
            cls.cachedModelRelations = cls.dbModel.modelRelations()
            cls.cachedModelRelationNames = cls.cachedModelRelations.keys()

    @classmethod
    def modelFields(cls):
        """
        Liefert die Felder des Models.

        :return: Dictionary mit Feldnamen:Feldobjekten
        """
        if cls.cachedModelFields is None:
            cls.cachedModelFields = cls.dbModel.modelFields()
        return cls.cachedModelFields

    @classmethod
    def modelFieldNames(cls):
        """
        Liefert die Felder des Models.

        :return: Dictionary mit Feldnamen:Feldobjekten
        """
        if cls.cachedModelFieldNames is None:
            cls.cachedModelFieldNames = cls.modelFields().keys()
        return cls.cachedModelFieldNames

    @classmethod
    def setDefaultValues(cls, object):
        """
        Lädt die Defaultwerte des Models und legt diese als Attribute/Werte an
        """
        if cls.dbModelDefaultValues is None:
            cls.dbModelDefaultValues = dict(
                (fieldName, field.defaultValue()) for fieldName, field in cls.modelFields().items()
            )
        object.loadFromDict(cls.dbModelDefaultValues)

    def __init__(self, dataDict=None, defaultValues=True, db=None):
        """
        Konstruktor der DbDataClass. Durch Angabe des dataDict Dictionaries,
        wird das Objekt mit den darin enthaltenen AttributName:Wert Einträgen erstellt.
        :param dataDict: Dictionary mit AttributName:Wert Einträgen
        :param args:
        :param kwargs:
        """

        self.__changeDetectionEnabled = False
        self.__originalAttributeValues = {}
        self.__changes = {}
        self.dataChanged = DbSignal()
        DbBareDataClass.__init__(self, dataDict=dataDict)
        self.db = db
        if defaultValues:
            self.setDefaultValues(self)

        if dataDict is not None:
            self.loadFromDict(dataDict=dataDict)

    def saveOriginalValues(self):
        self.__originalAttributeValues = self.__dict__.copy()

    def setChangeDetectionEnabled(self, enabled):
        """
        Schaltet die ChangeDetection an oder aus.
        :param enabled: bool ChangeDetection an/aus bzw. True/False
        """
        if enabled:
            # Kopie der Attribute anlegen um Original-Zustand zu behalten
            self.saveOriginalValues()
        self.__changeDetectionEnabled = enabled

    def isEqual(self, compareObject):
        """
        Vergleicht das übergebene Objekt mit den eigenen Daten und liefert
        True wenn das Objekt das gleiche Model benutzt und die Felder über die
        gleichen Daten verfügt. Bei einer Abweichung wird False zurueckgeliefert.

        :param compareObject: DbDataClass
        :return: bool
        """
        if self.dbModel != compareObject.dbModel:
            return False

        for modelFieldName in self.modelFields().keys():
            if getattr(compareObject, modelFieldName) != getattr(self, modelFieldName):
                return False

        return True

    def compareObjectChanges(self, compareObject):
        """
        Vergleicht das übergebene Objekt mit den eigenen Daten und liefert
        ein Dictionary mit Unterschiedenen in den Attributwerten verglichen mit
        den eigenen Attributwerten.

        :param compareObject:
        :return: dict Dictionary mit Unterschieden als Attributname:Wert Paaren.
        """
        ret = {}
        for modelFieldName in self.modelFields().keys():
            if getattr(compareObject, modelFieldName) != getattr(self, modelFieldName):
                ret[modelFieldName] = getattr(compareObject, modelFieldName)
        return ret

    def __setattr__(self, key, value):
        """
        Überladene Magic-Funktion zum beschreiben der Objekt-Attribute.
        Wenn changeDetectionEnabled auf True steht werden alle Änderungen an Attributen
        registriert und einem Changedictionary angehangen.

        :param key: str Attributname
        :param value: mixed Wert
        """

        if key[0] == "_":
            object.__setattr__(self, key, value)
            return

        # kein internes Attribut
        if not self.__changeDetectionEnabled:
            object.__setattr__(self, key, value)
            return

        # ChangeDetection aktiviert
        # Ueberpruefen ob es sich um ein ModelField handelt.
        if key not in self.modelFieldNames():
            object.__setattr__(self, key, value)
            return

        # Uerpruefen ob sich der Wert geaendert hat
        if type(value) == float and type(self.__dict__[key]) == float:
            changed = not isEqual(value, self.__dict__[key])
        else:
            changed = value != self.__dict__[key]

        if changed:
            if value == self.__originalAttributeValues[key] and key in self.__changes.keys():
                # Das Attribut befindet sich in der Changelist und wurde auf Original-Wert zurückgesetzt,
                # welches zum Zeitpunkt der ChangeDetection Aktivierung gesetzt war. Das Attribut muss aus
                # der Changelist geloescht werden, da kein Update noetig ist.
                del self.__changes[key]
            else:
                # Attribut wurde geändert und muss auf die Changelist.
                self.__changes[key] = value

            object.__setattr__(self, key, value)
            self.dataChanged.emit(self, key, value)
            return

        return

    def changes(self):
        """
        Liefert die Unterschiede die durch die Change Detection ermittelt wurden
        als Dictionary.

        :return: dict Dictionary mit Unterschieden als Attributname:Wert Paaren.
        """
        return self.__changes

    def originalValues(self):
        return self.__originalAttributeValues

    def resetChanges(self):
        """
        Ermöglicht von aussen, die Changes zu reseten

        :return: None
        """
        self.__changes = {}

    def hasChanged(self):
        """
        Liefert zurück, ob sich das Objekt während der ChangeDetection geändert hat

        :return: bool
        """
        return True if len(self.__changes) != 0 else False

    def modelDataDict(self):
        """
        Liefert ein Dictionary mit allen im Model definierten Feldern und ihren dazugehörigen
        Daten.

        :return:  dict Dictionary mit Modeldaten als Feldname:Wert Paaren.
        """
        ret = {}
        fieldNames = self.dbModel.modelFields().keys()
        for fieldName in fieldNames:
            ret[fieldName] = getattr(self, fieldName)
        return ret

    def jsonModelData(self):
        ret = {}
        data_dict = self.modelDataDict()
        for key in sorted(data_dict):
            data = data_dict[key]
            if isinstance(data, (str, str)):
                if isinstance(data, str):
                    data = data.encode("utf8")
            # elif isinstance(data, datetime.datetime):
            #     data = data.isoformat()
            if not isinstance(data, type):
                ret[key] = data
        return ret

    def primaryKeyValues(self):
        """
        Liefert den Wert des Primärschlüssels

        :return: value
        """
        pk = self.dbModel.primaryKey()
        primaryKeyValues = dict((fieldName, getattr(self, fieldName)) for fieldName in pk.fields().keys())
        if any(x == None for x in primaryKeyValues.values()):
            return None
        else:
            return primaryKeyValues

    def primaryKeyRepresentation(self):
        return self.dbModel.primaryKey().getStringRepresentation(self.primaryKeyValues())

    def primaryKeyValuesFromRepresentation(self, string):
        return self.dbModel.primaryKey().primaryKeyValuesFromRepresentation(string)

    def __getattribute__(self, name):
        mclass = object.__getattribute__(self, "__class__")
        mclass.cachedModelRelationsLock.acquire()
        if not mclass.cachedModelRelations:
            mclass.cachedModelRelations = mclass.dbModel.modelRelations()
            mclass.cachedModelRelationNames = mclass.cachedModelRelations.keys()
        mclass.cachedModelRelationsLock.release()

        # print self.__class__.cachedModelRelationNames

        if name[0] == "_":
            return object.__getattribute__(self, name)
        elif name not in mclass.cachedModelRelationNames:
            return object.__getattribute__(self, name)
        else:

            # if name not in dir(self):
            attrValue = mclass.cachedModelRelations[name].getRelationData(self)
            if attrValue is None:
                return None
            else:
                return attrValue
                #     setattr(self, name, attrValue)
                #
                # return object.__getattribute__(self, name)


class DbSingletonClass(with_metaclass(DbSingletonMetaClass, DbDataClass)):
    """
    Basic Klasse für Db Single Instance Objekte
    """
    modelPath = ""
    autoGeneratePrimaryKeyValues = False
    dbModel = None
    dataClass = None
    cachedFieldNames = None
    cachedPrimaryKeyFieldNames = None
    cachedGetAvailablePrimaryKeysSQL = None
    cachedSQLFieldNames = None
    numberRange = None
    changeCommitHooks = {}
    postChangeCommitHooks = {}
    parentSingletonClass = None

    @classmethod
    def ChangeCommitHook(cls, className):
        def realHook(func):
            cls.addChangeCommitHook(className, func)

        return realHook

    @classmethod
    def PostChangeCommitHook(cls, className):
        def realHook(func):
            cls.addPostChangeCommitHook(className, func)

        return realHook

    @classmethod
    def addChangeCommitHook(cls, className, func):
        if className not in cls.changeCommitHooks:
            cls.changeCommitHooks[className] = []
        cls.changeCommitHooks[className].append(func)

    @classmethod
    def addPostChangeCommitHook(cls, className, func):
        if className not in cls.postChangeCommitHooks:
            cls.postChangeCommitHooks[className] = []
        cls.postChangeCommitHooks[className].append(func)

    @classmethod
    def processChangeCommitHooks(cls, obj=None, values=None, oldValues=None):
        className = obj.__class__.__name__
        if className in cls.changeCommitHooks:
            for hook in cls.changeCommitHooks[className]:
                hook(obj=obj, values=values, oldValues=oldValues)

    @classmethod
    def processPostChangeCommitHooks(cls, obj=None, values=None, oldValues=None):
        className = obj.__class__.__name__
        if className in cls.postChangeCommitHooks:
            for hook in cls.postChangeCommitHooks[className]:
                hook(obj=obj, values=values, oldValues=oldValues)

    @classmethod
    def getNextID(cls, db=None):
        return db.getNextID(cls.numberRange)

    @classmethod
    def getNextNumber(cls, db=None):
        return db.getNextNumber(cls.numberRange)

    @classmethod
    def getNextAutoIncrement(cls, db=None):
        selectAutoinc = """
                select auto_increment from information_schema.tables
                where table_name = '%s'
                and table_schema = DATABASE()""" % cls.dbModel.dbTableName
        return db.dbQueryDict(selectAutoinc)[0]["auto_increment"]

    @classmethod
    def getChildClasses(cls):
        return dict((c.__name__, c) for c in cls.__subclasses__())

    @classmethod
    def getSingletonClassByName(cls, name):
        if name not in cls.getChildClasses():
            LOG.debug("dynamic import of {path}.{name}".format(name=name, path=cls.modelPath))
            __import__("{path}.{name}".format(name=name, path=cls.modelPath), fromlist=[name])
            # return None
        return cls.getChildClasses()[name]

    @classmethod
    def getAvailablePrimaryKeysSQL(cls):
        if cls.cachedGetAvailablePrimaryKeysSQL is None:
            sql = "select %s from %s" % (
                ",".join(cls.getPrimaryKeyFieldNames()),
                cls.dbModel.dbTableName
            )
            cls.cachedGetAvailablePrimaryKeysSQL = sql
        return cls.cachedGetAvailablePrimaryKeysSQL

    @classmethod
    def getAvailablePrimaryKeys(cls, db, filter={}):
        """
        Liefert eine Liste mit den vorhandenen Primärschlüsseln innerhalb des DbModels

        :param db: Db Objekt
        :return: Liste mit Primärschlüsseln
        """
        if len(filter) != 0:
            where = cls.dbModel.parseFilter(filter)
            where = " where " + where if len(where) != 0 else ""
        else:
            where = ""
        msql = cls.getAvailablePrimaryKeysSQL() + where
        return db.dbQueryDict(msql)

    @classmethod
    def syncDelete(cls, srcDb, dstDb):
        """
        Es werden die Datensätze auf dem Zielsystem gelöscht, die im vergleich zum Quellsystem
        überzäglig sind.
        :param srcDb:
        :param dstDb:
        :return:
        """
        srcPKList = list(str(x) for x in cls.getAvailablePrimaryKeys(db=srcDb))
        dstPKList = list(str(x) for x in cls.getAvailablePrimaryKeys(db=dstDb))

        diffPKList = list(set(dstPKList) - set(srcPKList))

        objs = cls.getMultipleRecords(db=dstDb, listPrimaryKeys=list(eval(x) for x in diffPKList))
        for obj in objs:
            obj.deleteInDatabase()

        return diffPKList

    @classmethod
    def getMultipleRecordsByFilter(cls, db, filter={}):
        """
        Liefert eine Liste mit den vorhandenen Primärschlüsseln innerhalb des DbModels

        :param db: Db Objekt
        :return: Liste mit Primärschlüsseln
        """

        # cachen der fieldListe des Models
        if cls.cachedSQLFieldNames is None:
            fieldNames = []
            for name, field in cls.dbModel.modelFields().items():
                if not isinstance(field, DbModelDummyField):
                    fieldNames.append(name)
            cls.cachedSQLFieldNames = ",".join(fieldNames)

        tableName = cls.dbModel.dbTableName
        filter = cls.dbModel.parseFilter(filter)
        filter = DbFilter.parseFilter(filter)
        where = " and ".join(list("%s %s" % (key, value) for key, value in filter.items()))
        where = "where " + where if len(where) != 0 else ""
        msql = "select %s from %s %s" % (cls.cachedSQLFieldNames, tableName, where)
        ret = cls.getMultipleRecordsBySQL(db=db, sql=msql)
        # print msql
        return ret

    @classmethod
    def getMultipleRecordsWhere(cls, db, whereClause=""):
        where = "where %s" % whereClause if whereClause != "" else ""
        ret = cls.getMultipleRecordsBySQL(
            db=db,
            sql="select %s from %s %s" % (
                ",".join(cls.dbModel.modelFields().keys()),
                cls.dbModel.dbTableName,
                where
            )
        )

        return ret

    @classmethod
    def getMultipleRecords(cls, db=None, listPrimaryKeys=[]):
        """
        Liefert die SingletonObjekte zu den in listPrimaryKeys angegeben Primärschlüsseln.
        Falls ein PrimaryKey nicht gefunden werden sollte, so ist die Rückgabe ohne ein
        entsprechendes Objekt.

        :param db: Db Objekt
        :param listPrimaryKeys: Liste mit Primärschlüsseln
        :return: Liste mit Objekten die gefunden wurden.
        """
        if len(listPrimaryKeys) == 0:
            return []

        pkFields = cls.dbModel.primaryKey().fields()
        tableName = cls.dbModel.dbTableName + "."
        pkFieldNames = cls.dbModel.primaryKey().fields().keys()

        pkTuppleStrings = []
        for pk in listPrimaryKeys:
            listPkData = []
            for fieldName in pkFieldNames:
                listPkData.append(pkFields[fieldName].convertForSQL(pk[fieldName]))
            pkTuppleStrings.append("(%s)" % ",".join(listPkData))

        inClause = "(%s) in (%s)" % (",".join(list(tableName + x for x in pkFieldNames)), ",".join(pkTuppleStrings))

        return cls.getMultipleRecordsWhere(db, inClause)

    @classmethod
    def getPrimaryKeyFieldNames(cls):
        if cls.cachedPrimaryKeyFieldNames is None:
            cls.cachedPrimaryKeyFieldNames = cls.dbModel.primaryKey().fields().keys()
        return cls.cachedPrimaryKeyFieldNames

    @classmethod
    def getMultipleRecordsBySQL(cls, db, sql):
        """

        :param db:
        :param sql:
        :return:
        """
        # print sql
        primaryKeyFieldNames = cls.getPrimaryKeyFieldNames()
        dataDicts = db.dbQueryDict(sql)
        ret = list(
            cls(
                db=db,
                primaryKeyValues=dict(
                    (fieldName, dataDict[fieldName]) for fieldName in primaryKeyFieldNames
                ),
                dataDict=dataDict,
                loadFromDatabase=False,
                overrideAutoCommit=True
            ) for dataDict in dataDicts
        )
        return ret

    @classmethod
    def getRecordFromJson(cls, db, json):
        primaryKeyFieldNames = cls.getPrimaryKeyFieldNames()
        return cls(
            db=db,
            primaryKeyValues=dict(
                (fieldName, json[fieldName]) for fieldName in primaryKeyFieldNames
            ),
            dataDict=json,
            loadFromDatabase=False,
            overrideAutoCommit=True
        )

    @classmethod
    def createUpdateStatement(cls, dataDict={}, primaryKeyValues={}):
        """
        Erzeugt ein SQL-Update-Statement durch Angabe eines Dictonaries mit
        Feldnamen und Werten sowie der Angabe des Primärschlüssel Wertes des
        zu ändernden Datensatzes.

        :param dataDict: dict mit Feldname zu FeldWert Einträgen
        :param primaryKeyValue: value Wert des PrimaryKeys.
        :return:
        """

        em = cls.dbModel
        mf = em.modelFields()
        pk = em.primaryKey()

        updateStrings = []
        for fieldName, value in dataDict.items():
            # print fieldName, mf[fieldName], value
            updateStrings.append("%s=%s" % (fieldName, mf[fieldName].convertForSQL(value)))

        updateClause = ",".join(updateStrings)
        # whereClause = em.parseFilter(primaryKeyValues)
        filter = em.parseFilter(primaryKeyValues)
        filter = DbFilter.parseFilter(filter)
        where = " and ".join(list("%s %s" % (key, value) for key, value in filter.items()))
        where = "where " + where if len(where) != 0 else ""

        statement = "update %s set %s %s" % (
            cls.dbModel.dbTableName,
            updateClause,
            where
        )
        return statement

    @classmethod
    def generatePrimaryKeyValues(cls, db=None):

        primaryKey = cls.dbModel.primaryKey()
        if len(primaryKey.fields()) == 1:
            nextID = cls.getNextID(db=db)
            primaryKeyValues = {primaryKey.fields().keys()[0]: nextID}
        else:
            raise ValueError("PrimaryKey cannot be autogenerated")
        return primaryKeyValues

    def __init__(self, db, primaryKeyValues={}, dataDict={}, loadFromDatabase=True, unbound=False,
                 defaultValues=False, overrideAutoCommit=None):
        """
        Erzeugt eine Objektinstanz einer DbSingletonClass.
        Es muss ein Db System sowie der Wert des PrimaryKeys uebergeben
        werden. Nach erstellen der Instanz werden die Daten aus der Datenbank
        geladen. Falls es schon eine Instanz zu diesem Primärschlüssel gibt, wird
        eine Referenz auf das schon existierende Objekt im Speicher gegeben. Das
        verwalten der Singleton Funktionalität übernimmt die Meta-Klasse.

        :param args:
        :param kwargs:  db=Db-Objekt , primaryKeyValue=Wert des Primärschluessels
        """
        # ganz wichtig __autoCommitEnabled muss als aller erstes gesetzt werden
        # sonst gibnts kabauf bei __setattr__. Noch bevor die Konstruktoren der Superklassen
        # aufgerufen werden.
        self.__autoCommitEnabled = False
        DbDataClass.__init__(self, defaultValues=True)
        self.db = db
        self.unbound = unbound

        self.loadFromDict(dataDict=dataDict)

        if not loadFromDatabase:
            self.setAutoCommitEnabled(False)
        else:
            self.setAutoCommitEnabled(True)

        self.initOk = True
        if overrideAutoCommit is not None:
            self.setAutoCommitEnabled(overrideAutoCommit)

        self.setChangeDetectionEnabled(True)

    # def __del__(self):
    #     print "delete"

    def __repr__(self):
        """
        Liefert eine Stringrepräsentation des Objektes inklusive der ID und dem System-Namen.
        :return: str
        """
        if self.unbound:
            return "<%s %s unbound %i>" % (self.__class__.__name__, self.db.systemName, id(self))
        else:
            return "<%s %s %s %i>" % (
                self.__class__.__name__, self.db.systemName, self.primaryKeyValues(), id(self))

    def __setattr__(self, key, value):
        # if not key[0] in ("_", "db"):
        if not key[0] == "_":
            if hasattr(self, "initOk"):
                if self.initOk:
                    if self.db.hooksEnabled:
                        if key in self.modelFieldNames():
                            self.modelFields()[key].processAttributeHooks(obj=self, value=value,
                                                                          oldValue=self.__dict__[key],
                                                                          fieldName=key)
            DbDataClass.__setattr__(self, key, value)
            if self.__autoCommitEnabled:
                if key in self.modelFields().keys():
                    if not isinstance(self.modelFields()[key], DbModelDummyField):
                        self.commit()
        else:
            DbDataClass.__setattr__(self, key, value)

    @classmethod
    def loadFromDatabase(cls, db, primaryKeyValues):
        """
        Lädt Felddaten des Datensatzes von der Datenbank

        :param db: Db Objekt
        :param primaryKeyValue: Wert des PrimaryKeys um von der Datenbank zu lesen
        """

        msql = cls.dbModel.getQuerySQL(primaryKeyValues)
        r = db.dbQueryDict(msql)
        if len(r) != 0:
            return r[0]
        else:
            raise DbRecordNotFoundError(cls=cls, db=db, primaryKeyValues=primaryKeyValues)

    def reloadFromDatabase(self):
        """
        Lädt erneut die Daten aus der Datenbank.
        """
        oldAutoCommit = self.autoCommitEnabled()
        if oldAutoCommit:
            self.setAutoCommitEnabled(False)

        dataDict = self.loadFromDatabase(db=self.db, primaryKeyValues=self.primaryKeyValues())
        self.loadFromDict(dataDict=dataDict)

        self.setAutoCommitEnabled(oldAutoCommit)

    def deleteInDatabase(self):
        where = self.dbModel.primaryKey().getWhereStatement(self.primaryKeyValues())
        if where != "":
            msql = "delete from %s where %s" % (self.dbModel.dbTableName, where)
            self.db.dbQueryDict(msql)
            DbSingletonMetaClass.deleteClassInstance(self)

    def setAutoCommitEnabled(self, enabled):
        """
        Schaltet AutoCommit ein oder aus.
        :param enabled:
        """
        self.__autoCommitEnabled = enabled

    def autoCommitEnabled(self):
        """
        Liefert zurueck ob AutoCommit enabled ist oder nicht.

        :return: bool
        """
        return self.__autoCommitEnabled

    def commit(self):
        """
        Schreibt die Änderungen am Objekt in die Datenbank und setzt das Changes Dictionary zurueck.
        """
        changes = self.changes()
        modelFields = self.modelFields()
        originalValues = self.originalValues()

        if len(changes) != 0:
            if self.db.hooksEnabled:
                self.processChangeCommitHooks(obj=self, values=changes, oldValues=originalValues)

                for fieldName, value in changes.items():
                    modelField = modelFields[fieldName]
                    changes[fieldName] = modelField.processChangeCommitHooks(obj=self, value=value,
                                                                             oldValue=originalValues[fieldName])

            self.commitToBackend(changes)
            self.resetChanges()
            self.saveOriginalValues()

            if self.db.hooksEnabled:
                self.processPostChangeCommitHooks(obj=self, values=changes, oldValues=originalValues)

    def commitToBackend(self, changes):
        sql = self.createUpdateStatement(changes, self.primaryKeyValues())
        # print sql
        self.db.dbQueryDict(sql)

    def updateFromDataObject(self, dataObj):
        """
        Uebernimmt Attribute von ubergebenen DbDataClass Objekt und updated die die Datenbank
        sofern Autocommit ein ist. Das übergebene Objekt muss nicht das selbe DbModel haben, es
        werden nur die in beiden Models enthaltenen Felder übernommen.

        :param dataObj: DbDataClass
        """
        ret = False

        primaryFieldNames = self.dbModel.primaryKey().fields().keys()
        # ermitteln der Felder die in beiden Models vorhanden sind
        commonFieldNames = list(set(self.dbModel.modelFields()) & set(dataObj.dbModel.modelFields()))
        # primaryKey Felder ausschliessen, diese dueren nicht ueberschrieben werden.
        commonFieldNames = list(set(commonFieldNames) - set(primaryFieldNames))
        # ermiteln der Changes
        oldAutoCommitEnabled = self.autoCommitEnabled()

        self.setAutoCommitEnabled(False)

        for fieldName in commonFieldNames:
            newValue = getattr(dataObj, fieldName)
            oldValue = getattr(self, fieldName)
            if oldValue != newValue:
                # wert hat sich geändert change merken und attribut updaten.
                # print "\t", fieldName, oldValue, newValue
                setattr(self, fieldName, newValue)
                ret = True

        if oldAutoCommitEnabled:
            self.commit()

        self.setAutoCommitEnabled(oldAutoCommitEnabled)
        return ret

    def create(self, autoCommitEnabled=True):
        """
        Erzeugt das Unbound Object in der Datenbank und
        wandelt es in ein Bound Object um.

        WICHTIG!!!!
        Sollte es überladen werden, muss DbSingletonMetaClass.bind
        aufgerufen werden damit das Object im Cache landet.

        :param autoCommitEnabled:
        """
        autoIncrementFieldName = None

        pk = self.dbModel.primaryKey()
        fields = self.dbModel.modelFields().copy()

        for fieldName in pk.fields():
            field = fields[fieldName]
            value = getattr(self, fieldName)

            if field.extra() == "on update CURRENT_TIMESTAMP":
                del fields[fieldName]
                continue

            if "auto_increment" in field.extra().split():
                autoIncrementFieldName = fieldName

            if autoIncrementFieldName != fieldName and value is None:
                raise Exception("PrimaryKeyValues not complete. %s is None" % fieldName)
                break

        listFieldNames = fields.keys()
        if autoIncrementFieldName:
            listFieldNames.remove(autoIncrementFieldName)
            del fields[autoIncrementFieldName]

        fieldNames = ",".join(listFieldNames)

        strValues = list(fields[fieldName].convertForSQL(getattr(self, fieldName)) for fieldName in listFieldNames)
        values = ",".join(strValues)

        dbConnection = self.db.dbGetConnection()
        msql = "insert into %s(%s) values(%s)" % (self.dbModel.dbTableName, fieldNames, values)
        # print msql
        dbConnection.dbQuery(msql)

        if autoIncrementFieldName:
            id = dbConnection.dbQuery("SELECT LAST_INSERT_ID() FROM %s" % self.dbModel.dbTableName)[0][0]
            setattr(self, autoIncrementFieldName, id)
        dbConnection.release()

        DbSingletonMetaClass.bind(self)
        self.setAutoCommitEnabled(autoCommitEnabled)

    def getSingletonObject(self):
        singletonClassName = self.dbModel.singletonClass
        if singletonClassName is None:
            return self
        else:
            singletonClass = DbSingletonClass.getChildClasses()[singletonClassName]
            return singletonClass(db=self.db, primaryKeyValues=self.primaryKeyValues())

    def syncToSystem(self, dstDb, overwriteExisting=True, createNotExisting=True, overwriteOnlyIfNewer=False):
        returnDict = {}

        try:
            dstObj = self.__class__(
                db=dstDb,
                primaryKeyValues=self.primaryKeyValues(),
                loadFromDatabase=True,
                # dataDict=self.dataDict()
            )
            if overwriteExisting:
                if "UPDATED" in self.modelFields().keys():
                    if overwriteOnlyIfNewer:
                        if self.UPDATED <= dstObj.UPDATED:
                            return
            # update
            dstObj.updateFromDataObject(self)
            returnDict["updated"] = self.primaryKeyValues()

        except DbRecordNotFoundError as e:
            if createNotExisting:
                # neu anlage
                dstObj = e.getUnboundObject()
                dstObj.updateFromDataObject(self)
                dstObj.create()
                returnDict["created"] = self.primaryKeyValues()

        return returnDict

    @classmethod
    def getUpdatedAfter(cls, db=None, startDate=None, withCheck=True, additionalWhere=None):
        if withCheck:
            if "UPDATED" not in cls.dbModel.modelFields():
                raise AttributeError("getUpdatedAfter not supported by:", cls.__class__)

        whereParts = ["UPDATED > \"%s\" " % dateTimeToMysqlStr(startDate)]
        if additionalWhere:
            whereParts.append(additionalWhere)
        where = " and ".join(whereParts)

        objs = cls.getMultipleRecordsWhere(
            db=db,
            whereClause=where
        )
        return objs

    @classmethod
    def SyncByPrimaryKey(cls):
        pass

    @classmethod
    def syncUpdatedAfter(cls, sourceSystem, destinationSystem, startDate=None, oneway=True, overwriteExisting=True,
                         createNotExisting=True, overwriteOnlyIfNewer=False, withCheck=True, syncDelete=False,
                         log=None):
        """
        Updated die momentan geladenen Inhalte der Klasse in abhängigkeit von source und destination System.

        :param sourceSystem: db Herkunftssystem aus dem die Daten synchronisiert werden sollen
        :param destinationSystem: db Zielsystem in das synchronisiert werden soll
        :param startDate: datetime Zeitpunkt ab dem synchronisiert wernden soll
        :param oneway: bool
            False: Es wird auf beiden Systemen je nach bedingung geupdated/neuanlage getätigt
            True: Je nach bedingung nur auf targetSystem updated/neuanlage
        :param overwriteExisting: bool
            True: Vorhanden Daten auf dem targetSystem werden überschrieben
        :param createNotExisting: bool
            True: Neuanlage des Datensatzes auf targetSystem
        :param overwriteOnlyIfNewer: bool
            True: Überschreibt nur Datensatz, wenn dessen UPDATED Feld neuer ist, als der vom Zielsystem

        :return: dict
            src: Alle PrimaryKeys der Obj. die im SourceSystem gefunden wurden
            dst: Alle PrimaryKeys der Obj. die im DestinationSystem gefunden wurden
            conflicts: PrimaryKeys aus beiden System, die Probleme aufweisen


        """
        # struktur rückgabe parameter
        src = {
            "pk": [],
            "values": {
                "updated": None,
                "created": None,
                "deleted": None
            },
            "conflicts": []
        }
        dst = src.copy()

        systemLogFromToStr = "[%s][%s]" % (sourceSystem.systemName, destinationSystem.systemName)
        systemLogToFromStr = "[%s][%s]" % (destinationSystem.systemName, sourceSystem.systemName)
        conflictPks = []
        sourceSystem.dbConnect()
        destinationSystem.dbConnect()
        tableName = cls.dbModel.dbTableName.upper()

        if log:
            tableLogStr = "%s[%s]" % (systemLogFromToStr, tableName)
            log("%s Sync started." % tableLogStr)

        if startDate is not None:
            srcObjs = cls.getUpdatedAfter(db=sourceSystem, startDate=startDate, withCheck=withCheck)
            srcPks = list(obj.primaryKeyRepresentation() for obj in srcObjs)

            if not oneway:
                dstObjs = cls.getUpdatedAfter(db=destinationSystem, startDate=startDate, withCheck=withCheck)
                dstPks = list(obj.primaryKeyRepresentation() for obj in dstObjs)
                conflictPks = list(set(srcPks) & set(dstPks))

                if log:
                    tableLogStr = "%s[%s]" % (systemLogFromToStr, tableName)
                    log("%s Discovered %i records with conflicts." % (tableLogStr, len(conflictPks)))

                for pk in conflictPks:
                    srcObjs.remove(cls(db=sourceSystem, primaryKeyValues=eval(pk)))
                    dstObjs.remove(cls(db=destinationSystem, primaryKeyValues=eval(pk)))

            added = []
            updated = []
            for srcObj in srcObjs:
                syncOperation = srcObj.syncToSystem(
                    dstDb=destinationSystem,
                    overwriteExisting=overwriteExisting,
                    createNotExisting=createNotExisting,
                    overwriteOnlyIfNewer=overwriteOnlyIfNewer
                )
                if syncOperation is not None:
                    if "created" in syncOperation.keys():
                        added.append(syncOperation["created"])
                    if "updated" in syncOperation.keys():
                        updated.append(syncOperation["updated"])

            src["values"]["created"] = added
            src["values"]["updated"] = updated
            src["pk"].extend(srcPks)

            if log:
                tableLogStr = "%s[%s]" % (systemLogFromToStr, tableName)
                log("%s Created %i records." % (tableLogStr, len(added)))
                log("%s Updated %i records." % (tableLogStr, len(updated)))

            if not oneway:
                added = []
                updated = []
                for dstObj in dstObjs:
                    syncOperation = dstObj.syncToSystem(
                        dstDb=sourceSystem,
                        overwriteExisting=overwriteExisting,
                        createNotExisting=createNotExisting,
                        overwriteOnlyIfNewer=overwriteOnlyIfNewer
                    )
                    if syncOperation is not None:
                        if "created" in syncOperation.keys():
                            added.append(syncOperation["created"])
                        if "updated" in syncOperation.keys():
                            updated.append(syncOperation["updated"])

                dst["values"]["created"] = added
                dst["values"]["updated"] = updated
                dst["pk"].extend(dstPks)

                if log:
                    tableLogStr = "%s[%s]" % (systemLogToFromStr, tableName)
                    log("%s Created %i records." % (tableLogStr, len(added)))
                    log("%s Updated %i records." % (tableLogStr, len(updated)))

            else:
                if syncDelete:
                    deletePks = cls.syncDelete(srcDb=sourceSystem, dstDb=destinationSystem)
                    src["pk"].extend(deletePks)
                    src["values"]["delete"] = deletePks

                    if log:
                        tableLogStr = "%s[%s]" % (systemLogFromToStr, tableName)
                        log("%s Deleted %i records." % (tableLogStr, len(deletePks)))

            returnDict = {
                "src": src,
                "dst": dst,
                "conflicts": conflictPks
            }

            sourceSystem.dbClose()
            destinationSystem.dbClose()

            if log:
                tableLogStr = "%s[%s]" % (systemLogFromToStr, tableName)
                log("%s Sync finished." % tableLogStr)

            return returnDict

    @classmethod
    def sync(cls, sourceSystem, destinationSystem, startDate=None, oneway=False, overwriteExisting=True,
             createNotExisting=True, overwriteOnlyIfNewer=False, withLogEntry=True, syncDelete=False, log=None):
        # muss überladen werden
        pass

    def log(self, logClassObj):
        self.modifyLogClassObject(logClassObj)
        return logClassObj.create()

    def modifyLogClassObject(self, logClassObj):
        logClassObj.setDb(db=self.db)
        logClassObj.setObjInstance(objInstance=self)
        return logClassObj


class DbQueryModelField(DbModelField):
    def __init__(self, singletonClassString, fieldName, converter=None):
        self.__singletonClass = DbSingletonClass.getChildClasses()[singletonClassString]
        self.__relatedField = self.__singletonClass.dbModel.modelFields()[fieldName]
        self.__relatedFieldName = fieldName
        self.__relatedTableName = self.__singletonClass.dbModel.dbTableName

        if converter is None:
            converter = self.__relatedField.converter()

        super(DbQueryModelField, self).__init__(
            caption=self.__relatedField.caption(),
            fieldType=self.__relatedField.fieldType(),
            defaultValue=self.__relatedField.defaultValue(),
            converter=converter
        )

    def relatedFieldName(self):
        return self.__relatedFieldName

    def relatedTableName(self):
        return self.__relatedTableName


class DbQueryModel(DbModel):
    def __init__(self):
        DbModel.__init__(self)

    @classmethod
    def getQueryWhere(cls, primaryKeyValues):
        where = " and ".join(
            list(
                "%s.%s = %s" % (
                    cls.dbTableName,
                    fieldName,
                    cls.modelFields()[fieldName].convertForSQL(value)
                ) for fieldName, value in primaryKeyValues.items()
            )
        )
        where = " where " + where if where != "" else ""
        return where

    @classmethod
    def getQuerySQL(cls, primaryKeyValues):
        """
        Generiert ein SQL-Select-Statement zur Abfrage eines Datensatzes unter Angabe des
        Primärschlüssel-Wertes

        :param kwargs: Felder des PrimaryKeys
        :return: str SQL-Select-Statement
        """

        where = cls.getQueryWhere(primaryKeyValues)
        msql = cls.dbQuerySQL + where
        return msql

        # @classmethod
        # def parseFilter(cls, filter={}):
        #     modelFields = cls.modelFields()
        #     for key, value in filter.items():
        #         if not isinstance(value, Filter.DbFilter):
        #             filter[key] = "=" + modelFields[key].convertForSQL(value)
        #     return filter


class DbQueryClass(DbSingletonClass):
    @classmethod
    def getMultipleRecordsFilterSQL(cls, filter):

        filter = cls.dbModel.parseFilter(filter)
        filter = DbFilter.parseFilter(filter)

        map = {}
        for fieldName, field in cls.dbModel.modelFields().items():
            if fieldName in filter.keys():
                map[fieldName] = field

        filter = dict(
            (
                "%s.%s" % (field.relatedTableName(), field.relatedFieldName()),
                filter[fieldName]
            ) for fieldName, field in map.items()
        )

        where = " and ".join(list("%s %s" % (key, value) for key, value in filter.items()))
        where = "where " + where if len(where) != 0 else ""
        msql = cls.dbModel.dbQuerySQL + where
        return msql

    @classmethod
    def getMultipleRecordsByFilter(cls, db, filter={}):
        """
        Liefert eine Liste mit den vorhandenen Primärschlüsseln innerhalb des DbModels

        :param db: Db Objekt
        :return: Liste mit Primärschlüsseln
        """

        # cachen der fieldListe des Models
        if cls.cachedFieldNames is None:
            cls.cachedFieldNames = ",".join(cls.dbModel.modelFields().keys())

        msql = cls.getMultipleRecordsFilterSQL(filter)
        ret = cls.getMultipleRecordsBySQL(db=db, sql=msql)
        return ret

    def __init__(self, db, primaryKeyValues={}, dataDict={}, loadFromDatabase=True, defaultValues=False):
        super(DbQueryClass, self).__init__(db, primaryKeyValues, dataDict, loadFromDatabase, defaultValues)

    def loadFromDatabase(self, db, primaryKeyValues={}):
        """
        Lädt Felddaten des Datensatzes von der Datenbank

        :param db: Db Objekt
        :param primaryKeyValue: Wert des PrimaryKeys um von der Datenbank zu lesen
        """
        oldAutoCommit = self.autoCommitEnabled()
        self.setAutoCommitEnabled(False)

        msql = self.dbModel.getQuerySQL(primaryKeyValues)
        r = db.dbQueryDict(msql)

        if len(r) != 0:
            self.loadFromDict(dataDict=r[0])

        self.setAutoCommitEnabled(oldAutoCommit)

    def getSingletonObject(self):
        singletonClass = DbSingletonClass.getChildClasses()[self.dbModel.dbSingletonClass]
        obj = singletonClass(db=self.db, primaryKeyValues=self.primaryKeyValues())
        return obj


class DbModelManyToManyRelation(DbModelRelation):
    def __init__(self, singletonClass=None, combiningClass=None, relationName=None, filter={}):
        self.combiningClassName = combiningClass
        self.combiningClass = None
        self.relationName = relationName
        self.cachedTargetSelectSQL = None
        super(DbModelManyToManyRelation, self).__init__(singletonClass, filter)

    def getRelationData(self, obj):
        if self.cachedTargetSelectSQL is None:
            self.combiningClass = DbSingletonClass.getSingletonClassByName(self.combiningClassName)
            self.singletonClass = DbSingletonClass.getSingletonClassByName(self.singletonClassName)

            ccem = self.combiningClass.dbModel
            scem = self.singletonClass.dbModel
            scfn = list(
                "%s.%s" % (scem.dbTableName, fieldName) for fieldName in scem.modelFields().keys())
            # print scfn

            fieldNames = scfn

            selectStatement = "select " + ",".join(fieldNames) + " from " + ccem.dbTableName + " "
            selectStatement += ccem.getJoinClause(scem, self.relationName)
            self.cachedTargetSelectSQL = selectStatement

        selectStatement = self.cachedTargetSelectSQL

        generatedFilter = self.transformFilter(obj)
        filter = self.combiningClass.dbModel.parseFilter(generatedFilter)
        filter = DbFilter.parseFilter(filter)
        where = " and ".join(list("%s %s" % (key, value) for key, value in filter.items()))
        where = " where " + where if len(where) != 0 else ""

        selectStatement += where

        ret = self.singletonClass.getMultipleRecordsBySQL(
            db=obj.db,
            sql=selectStatement
        )
        return ret


class DbModelOneToOneRelation(DbModelRelation):
    """
    Basisklasse einer One-To-One Tabellen-Relation.

    Beispieldefinition:
        CART_ID = DbModelField("", int, 0)
        CART = DbModelOneToOneRelation(singletonClass=Cart, filter={"ID": CART_ID})

    """

    def getRelationData(self, obj):
        if self.singletonClass is None:
            self.singletonClass = DbSingletonClass.getSingletonClassByName(self.singletonClassName)

        generatedFilter = self.transformFilter(obj)

        # hier ne kopie machen denn das generatedFilter wird noch transformed
        pkValues = generatedFilter.copy()

        r = self.singletonClass.getMultipleRecordsByFilter(db=obj.db, filter=generatedFilter)
        if len(r) != 0:
            return r[0]

        if not self.newObjectIfNotFound:
            return None

        pkFieldNames = self.singletonClass.dbModel.primaryKey().fields().keys()
        filterKeys = pkValues.keys()

        if len(list(set(pkFieldNames) - set(filterKeys))) != 0:
            return None

        r = self.singletonClass(db=obj.db, primaryKeyValues=pkValues, loadFromDatabase=False)
        return r


class DbModelOneToManyRelation(DbModelRelation):
    """
    Basisklasse einer One-To-Many Tabellen-Relation.

    Beispieldefinition:
        ID = DbModelField("Id", int, 0)
        POSITIONS = DbModelOneToManyRelation(singletonClass=CartHasProduct, filter={"CART_ID": ID})

    """

    def getRelationData(self, obj):
        if self.singletonClass is None:
            self.singletonClass = DbSingletonClass.getSingletonClassByName(self.singletonClassName)
        generatedFilter = self.transformFilter(obj)
        r = self.singletonClass.getMultipleRecordsByFilter(db=obj.db, filter=generatedFilter)
        return r


from .Database import Database

from .Signal import DbSignal
