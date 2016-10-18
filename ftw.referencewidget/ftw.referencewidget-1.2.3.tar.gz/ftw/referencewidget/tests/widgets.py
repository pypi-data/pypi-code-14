from ftw.testbrowser.widgets.base import PloneWidget
from ftw.testbrowser.widgets.base import widget


@widget
class ReferenceBrowserWidget(PloneWidget):

    @staticmethod
    def match(node):
        if not node.tag == 'div' or 'field' not in node.classes:
            return False

        return bool(node.css('div.referencewidget'))

    def fill(self, values):
        field = self.css('input[type="hidden"]').first

        if isinstance(values, basestring):
            field.value = values
        else:
            # Assume an DX object
            field.value = '/'.join(values.getPhysicalPath())
