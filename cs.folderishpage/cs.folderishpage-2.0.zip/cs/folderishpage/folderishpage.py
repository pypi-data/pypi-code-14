from collective import dexteritytextindexer
from cs.folderishpage import MessageFactory as _
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five import BrowserView
from zope.interface import implements


# Interface class; used to define content-type schema.
class IFolderishPage(model.Schema, IImageScaleTraversable):
    """
    A folderish page
    """
    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u'Content'),
        required=False
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class FolderishPage(Container):
    implements(IFolderishPage)
    # Add your class methods and properties here


# View class
class FolderishPageView(BrowserView):
    pass


class FolderishPageWithContents(BrowserView):

    def contents(self):
        return IContentListing(self.context.getFolderContents())
