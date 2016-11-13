# datadelete.py
# Copyright 2016 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""ChessTab extensions of gridsup.gui.datadelete.

May put this back in gridsup.gui.datadelete or in new rmappsup class.

"""
# How general is need for self.oldview and interpretation of on_destroy()?
# Do not want to disturb gridsup package right now.

from gridsup.gui.datadelete import DataDelete
        

class DataDelete(DataDelete):
    
    """Provide ChessTab management of widget destruction for DataDelete.
    """

    def __init__(self, instance, parent, oldview, title):
        """Extend RecordDelete with dialogue widgets for delete instance."""
        super().__init__(instance, parent, oldview, title)
        parent.bind('<Destroy>', self.on_destroy)
        self.oldview = oldview

    def on_destroy(self, event=None):
        """Tidy up after destruction of dialogue widget and all children."""
        if event.widget == self.parent:
            self.tidy_on_destroy()

    def tidy_on_destroy(self):
        """Do nothing. Override as required."""
