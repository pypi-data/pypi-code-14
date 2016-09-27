from ftw.referencewidget.interfaces import IReferenceWidget
from z3c.form import converter
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.interfaces import IRelation

from zope.component import adapts


class ReferenceDataListConverter(converter.BaseDataConverter):

    adapts(IRelationList, IReferenceWidget)

    def toFieldValue(self, value):
        if not value:
            return
        elif isinstance(value, unicode):
            return [self.widget.context.unrestrictedTraverse(
                value.encode("utf8"))]
        else:
            result = []
            for item in value:
                if not item:
                    continue
                result.append(self.widget.context.unrestrictedTraverse(
                    item.encode("utf-8")))
            return result

    def toWidgetValue(self, value):
        result = []
        for item in value:
            result.append('/'.join(item.getPhysicalPath()))
        return result


class ReferenceDataChoiceConverter(converter.BaseDataConverter):

    adapts(IRelation, IReferenceWidget)

    def toFieldValue(self, value):
        if not value:
            return
        elif isinstance(value, unicode):
            return self.widget.context.unrestrictedTraverse(
                value.encode("utf8"))
        else:
            return self.widget.context.unrestrictedTraverse(
                value[0].encode("utf-8"))

    def toWidgetValue(self, value):
        if value:
            return '/'.join(value.getPhysicalPath())
