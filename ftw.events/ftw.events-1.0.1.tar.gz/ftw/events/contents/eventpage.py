from ftw.events.interfaces import IEventPage
from plone.app.event.dx.behaviors import IEventBasic
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.directives import form
from plone.supermodel.interfaces import FIELDSETS_KEY
from zope.interface import alsoProvides
from zope.interface import implements


# Move plone.app.event's default field "timezone" to the default schema,
# since all other fields are in the default schema and we do not want
# an extra schema only for the "timezone" field.
for fieldset in IEventBasic.queryTaggedValue(FIELDSETS_KEY, []):
    if 'timezone' in fieldset.fields:
        fieldset.fields.remove('timezone')


class IEventPageSchema(form.Schema):
    pass

alsoProvides(IEventPageSchema, IFormFieldProvider)


class EventPage(Container):
    implements(IEventPage)
