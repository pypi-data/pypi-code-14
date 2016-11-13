# dataedit.py
# Copyright 2016 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""ChessTab extensions of gridsup.gui.datashow.

May put this back in gridsup.gui.datashow or in new rmappsup class.

"""
# How general is need for self.oldview and interpretation of on_destroy()?
# The newview attribute should be defined alongside oldview attribute.
# Do not want to disturb gridsup package right now.

from gridsup.gui.dataedit import DataEdit
        

class DataEdit(DataEdit):
    
    """Provide an edit and insert record dialogue.
    """

    def __init__(
        self,
        newobject,
        parent,
        oldobject,
        newview,
        title,
        oldview=None,
        ):
        """Extend RecordEdit with dialogue widgets for edit objects."""
        super().__init__(
            newobject, parent, oldobject, newview, title, oldview=oldview)
        parent.bind('<Destroy>', self.on_destroy)
        self.oldview = oldview

    def on_destroy(self, event=None):
        """Tidy up after destruction of dialogue widget and all children."""
        if event.widget == self.parent:
            self.tidy_on_destroy()

    def tidy_on_destroy(self):
        """Do nothing. Override as required."""
