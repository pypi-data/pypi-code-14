from cadnano.cnproxy import UndoCommand
from cadnano.assembly import Assembly
from cadnano.part import Part
from cadnano.objectinstance import ObjectInstance

class AddRefObjectCommand(UndoCommand):
    """Undo ready command for adding an instance.

    Args:
        document (Document): m
        cnobj:
    """
    def __init__(self, document, cnobj):
        super(AddRefObjectCommand, self).__init__("Add Reference Object")
        self._document = document
        self._cnobj = cnobj
    # end def

    def redo(self):
        doc = self._document
        cnobj = self._cnobj
        cnobj.setDocument(doc)
        self._document.addRefObj(cnobj)
    # end def

    def undo(self):
        doc = self._document
        cnobj = self._cnobj
        doc.removeRefObj(cnobj)
        cnobj.setDocument(None)
    # end def
# end class
