# selectionrow.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Create widgets that display details of game selection rules on database.
"""

import tkinter

from gridsup.gui.datarow import DataRow
from gridsup.gui.datarow import GRID_COLUMNCONFIGURE, GRID_CONFIGURE
from gridsup.gui.datarow import WIDGET_CONFIGURE, WIDGET, ROW

from ..core.chessrecord import ChessDBrecordSelection
from .selectiondbedit import ChessDBeditSelection
from .selectiondbdelete import ChessDBdeleteSelection
from .selectiondbshow import ChessDBshowSelection
from . import constants

ON_DISPLAY_COLOUR = '#eba610' # a pale orange


class ChessDBrowSelection(ChessDBrecordSelection, DataRow):
    
    """Define row in list of game selection rules.

    Add row methods to the game selection rule record definition.
    
    """

    header_specification = [
        {WIDGET: tkinter.Label,
         WIDGET_CONFIGURE: dict(text='Description'),
         GRID_CONFIGURE: dict(column=0, sticky=tkinter.EW),
         GRID_COLUMNCONFIGURE: dict(weight=1, uniform='pp'),
         ROW: 0,
         },
        #{WIDGET: tkinter.Label,
        # WIDGET_CONFIGURE: dict(text='Rule'),
        # GRID_CONFIGURE: dict(column=1, sticky=tkinter.EW),
        # GRID_COLUMNCONFIGURE: dict(weight=1, uniform='pp'),
        # ROW: 0,
        # },
        ]

    def __init__(self, database=None, ui=None):
        """Extend and associate record definition with database.

        database - the open database that is source of row data
        ui - the ChessUI instamce

        """
        super(ChessDBrowSelection, self).__init__()
        self.ui = ui
        self.set_database(database)
        self.row_specification = [
            {WIDGET: tkinter.Label,
             WIDGET_CONFIGURE: dict(font=constants.LISTS_OF_GAMES_FONT),
             GRID_CONFIGURE: dict(column=0, sticky=tkinter.EW),
             ROW: 0,
             },
            #{WIDGET: tkinter.Label,
            # WIDGET_CONFIGURE: dict(font=constants.LISTS_OF_GAMES_FONT),
            # GRID_CONFIGURE: dict(column=1, sticky=tkinter.EW),
            # ROW: 0,
            # },
            ]
        
    def show_row(self, dialog, oldobject):
        """Return a ChessDBshowSelection dialog for instance.

        dialog - a Toplevel
        oldobject - a ChessDBrecordSelection containing original data

        """
        return ChessDBshowSelection(dialog, oldobject, ui=self.ui)
        
    def delete_row(self, dialog, oldobject):
        """Return a ChessDBdeleteSelection dialog for instance.

        dialog - a Toplevel
        oldobject - a ChessDBrecordSelection containing original data

        """
        return ChessDBdeleteSelection(dialog, oldobject, ui=self.ui)

    def edit_row(self, dialog, newobject, oldobject, showinitial=True):
        """Return a ChessDBeditSelection dialog for instance.

        dialog - a Toplevel
        newobject - a ChessDBrecordSelection containing original data to be
                    edited
        oldobject - a ChessDBrecordSelection containing original data
        showintial == True - show both original and edited data

        """
        return ChessDBeditSelection(
            newobject,
            dialog,
            oldobject,
            showinitial=showinitial,
            ui=self.ui)

    def grid_row(self, **kargs):
        """Return super().grid_row(textitems=(...), **kargs).

        Create textitems argument for ChessDBrowSelection instance.

        """
        return super(ChessDBrowSelection, self).grid_row(
            textitems=(
                self.value.get_name_text(),
                #self.value.get_selection_rule_text(
                #    delimiter=constants.SPACE_SEP),
                ),
            **kargs)

    def grid_row_on_display(self, **kargs):
        self._current_row_background = ON_DISPLAY_COLOUR
        return self.grid_row(background=ON_DISPLAY_COLOUR, **kargs)

    def set_background_on_display(self, widgets):
        self._current_row_background = ON_DISPLAY_COLOUR
        self.set_background(widgets, self._current_row_background)


def make_ChessDBrowSelection(chessui):
    """Make ChessDBrowSelection with reference to ChessUI instance"""
    def make_selection(database=None):
        return ChessDBrowSelection(database=database, ui=chessui)
    return make_selection
