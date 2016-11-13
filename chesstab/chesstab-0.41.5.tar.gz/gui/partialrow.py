# partialrow.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Create widgets that display details of partial positions on database.
"""

import tkinter

from gridsup.gui.datarow import DataRow
from gridsup.gui.datarow import GRID_COLUMNCONFIGURE, GRID_CONFIGURE
from gridsup.gui.datarow import WIDGET_CONFIGURE, WIDGET, ROW

from ..core.chessrecord import ChessDBrecordPartial
from .partialdbedit import ChessDBeditPartial
from .partialdbdelete import ChessDBdeletePartial
from .partialdbshow import ChessDBshowPartial
from . import constants

ON_DISPLAY_COLOUR = '#eba610' # a pale orange


class ChessDBrowPartial(ChessDBrecordPartial, DataRow):
    
    """Define row in list of partial positions.

    Add row methods to the partial position record definition.
    
    """

    header_specification = [
        {WIDGET: tkinter.Label,
         WIDGET_CONFIGURE: dict(text='Description'),
         GRID_CONFIGURE: dict(column=0, sticky=tkinter.EW),
         GRID_COLUMNCONFIGURE: dict(weight=1, uniform='pp'),
         ROW: 0,
         },
        {WIDGET: tkinter.Label,
         WIDGET_CONFIGURE: dict(text='Position'),
         GRID_CONFIGURE: dict(column=1, sticky=tkinter.EW),
         GRID_COLUMNCONFIGURE: dict(weight=1, uniform='pp'),
         ROW: 0,
         },
        ]

    def __init__(self, database=None, ui=None):
        """Extend and associate record definition with database.

        database - the open database that is source of row data
        ui - the ChessUI instamce

        """
        super(ChessDBrowPartial, self).__init__()
        self.ui = ui
        self.set_database(database)
        self.row_specification = [
            {WIDGET: tkinter.Label,
             WIDGET_CONFIGURE: dict(font=constants.LISTS_OF_GAMES_FONT),
             GRID_CONFIGURE: dict(column=0, sticky=tkinter.EW),
             ROW: 0,
             },
            {WIDGET: tkinter.Label,
             WIDGET_CONFIGURE: dict(font=constants.LISTS_OF_GAMES_FONT),
             GRID_CONFIGURE: dict(column=1, sticky=tkinter.EW),
             ROW: 0,
             },
            ]
        
    def show_row(self, dialog, oldobject):
        """Return a ChessDBshowPartial dialog for instance.

        dialog - a Toplevel
        oldobject - a ChessDBrecordPartial containing original data

        """
        return ChessDBshowPartial(dialog, oldobject, ui=self.ui)
        
    def delete_row(self, dialog, oldobject):
        """Return a ChessDBdeletePartial dialog for instance.

        dialog - a Toplevel
        oldobject - a ChessDBrecordPartial containing original data

        """
        return ChessDBdeletePartial(dialog, oldobject, ui=self.ui)

    def edit_row(self, dialog, newobject, oldobject, showinitial=True):
        """Return a ChessDBeditPartial dialog for instance.

        dialog - a Toplevel
        newobject - a ChessDBrecordPartial containing original data to be edited
        oldobject - a ChessDBrecordPartial containing original data
        showintial == True - show both original and edited data

        """
        return ChessDBeditPartial(
            newobject,
            dialog,
            oldobject,
            showinitial=showinitial,
            ui=self.ui)

    def grid_row(self, **kargs):
        """Return super(ChessDBrowPartial,).grid_row(textitems=(...), **kargs).

        Create textitems argument for ChessDBrowPartial instance.

        """
        return super(ChessDBrowPartial, self).grid_row(
            textitems=(
                self.value.get_name_text(),
                self.value.get_position_text(delimiter=constants.SPACE_SEP),
                ),
            **kargs)

    def grid_row_on_display(self, **kargs):
        self._current_row_background = ON_DISPLAY_COLOUR
        return self.grid_row(background=ON_DISPLAY_COLOUR, **kargs)

    def set_background_on_display(self, widgets):
        self._current_row_background = ON_DISPLAY_COLOUR
        self.set_background(widgets, self._current_row_background)


def make_ChessDBrowPartial(chessui):
    """Make ChessDBrowPartial with reference to ChessUI instance"""
    def make_partial(database=None):
        return ChessDBrowPartial(database=database, ui=chessui)
    return make_partial
