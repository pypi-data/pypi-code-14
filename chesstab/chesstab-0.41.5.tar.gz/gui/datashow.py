# datashow.py
# Copyright 2016 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""ChessTab extensions of gridsup.gui.datashow.

May put this back in gridsup.gui.datashow or in new rmappsup class.

"""
# How general is need for self.oldview and interpretation of on_destroy()?
# Do not want to disturb gridsup package right now.

from gridsup.gui.datashow import DataShow
        

class DataShow(DataShow):
    
    """Provide ChessTab management of widget destruction for DataShow.
    """

    def __init__(self, instance, parent, oldview, title):
        """Add tidy-up management after widget destruction."""
        super().__init__(instance, parent, oldview, title)
        parent.bind('<Destroy>', self.on_destroy)
        self.oldview = oldview

    def on_destroy(self, event=None):
        """Tidy up after destruction of dialogue widget and all children."""
        if event.widget == self.parent:
            self.tidy_on_destroy()

    def tidy_on_destroy(self):
        """Do nothing. Override as required."""
