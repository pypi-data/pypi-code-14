from Products.Archetypes import PloneMessageFactory as _
from Products.Archetypes.Schema import Schema
from Products.Archetypes.Field import StringField
from Products.Archetypes.Widget import SelectionWidget
from Products.Archetypes.config import TOOL_NAME
from Products.Archetypes.interfaces.ITemplateMixin import ITemplateMixin

from Products.CMFCore import permissions, utils
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Acquisition import aq_base
from Acquisition import aq_inner
from ExtensionClass import Base
from zope.interface import implements


TemplateMixinSchema = Schema((
    # TemplateMixin
    StringField('layout',
                write_permission=permissions.ModifyPortalContent,
                default_method="getDefaultLayout",
                vocabulary="_voc_templates",
                widget=SelectionWidget(label=_(u'label_template_mixin',
                                               default=u'View template'),
                                       description=_(u'help_template_mixin',
                                                     default=u'Choose a template that will be used for viewing this item.'),
                                       visible={'view': 'hidden',
                                                'edit': 'visible'},)
                ),
))


class TemplateMixin(Base):
    implements(ITemplateMixin)

    schema = TemplateMixinSchema

    actions = (
        {'id': 'view',
         'name': 'View',
         'action': 'string:${object_url}/',
         'permissions': (permissions.View,),
         },
    )

    aliases = {
        '(Default)': '',
        'index_html': '',
        'view': '',
        'gethtml': 'source_html',
    }

    # if default_view is None TemplateMixin is using the immediate_view from
    # the type information
    default_view = None
    suppl_views = ()

    security = ClassSecurityInfo()

    index_html = None  # setting index_html to None forces the usage of __call__

    def __call__(self):
        """return a view based on layout"""
        v = self.getTemplateFor(self.getLayout())
        # rewrap the template in the right context
        context = aq_inner(self)
        v = v.__of__(context)
        return v(context, context.REQUEST)

    def _voc_templates(self):
        at = utils.getToolByName(self, TOOL_NAME)
        return at.lookupTemplates(self)

    # BBB backward compatibility
    templates = _voc_templates

    security.declareProtected(permissions.View, 'getLayout')

    def getLayout(self, **kw):
        # Get the current layout or the default layout if the current one is
        # None.
        if 'schema' in kw:
            schema = kw['schema']
        else:
            schema = self.Schema()
            kw['schema'] = schema
        value = schema['layout'].get(self, **kw)
        if value:
            return value
        else:
            return self.getDefaultLayout()

    security.declareProtected(permissions.View, 'getDefaultLayout')

    def getDefaultLayout(self):
        # Get the default layout used for TemplateMixin.
        #
        # Check the class definition for a attribute called 'default_view' then
        # check the Factory Type Information (portal_types) for an attribute
        # immediate_view else finally return the 'base_view' string which is a
        # autogenerated form from Archetypes.
        default_view = getattr(aq_base(self), 'default_view', None)
        if default_view:
            return default_view
        immediate_view = getattr(self.getTypeInfo(), 'immediate_view', None)
        if immediate_view:
            return immediate_view
        return 'base_view'

    def getTemplateFor(self, pt, default='base_view'):
        # Let the SkinManager handle this.
        # But always try to show something.
        pt = getattr(self, pt, None)
        if not pt:
            # default is the value of obj.default_view or base_view
            default_pt = getattr(self, 'default_view', None)
            if not default_pt:
                default_pt = default
            return getattr(self, default_pt)
        else:
            return pt

InitializeClass(TemplateMixin)

# BBB backward compatibility
schema = TemplateMixinSchema
getTemplateFor = TemplateMixin.getTemplateFor

__all__ = ('TemplateMixinSchema', 'TemplateMixin', )
