from Products.Archetypes import atapi
from Products.CMFCore import utils
from zope.i18nmessageid import MessageFactory


PROJECTNAME = 'ftw.xlsxsaveadapter'
ADD_PERMISSIONS = {
    'XlsxDataAdapterSchema': 'ftw.xlsxsaveadapter: Add XlsxDataAdapter',
}


_ = MessageFactory(PROJECTNAME)


def initialize(context):

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PROJECTNAME),
        PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (PROJECTNAME, atype.portal_type),
                          content_types=(atype, ),
                          permission=ADD_PERMISSIONS[atype.portal_type],
                          extra_constructors=(constructor,),
                          ).initialize(context)
