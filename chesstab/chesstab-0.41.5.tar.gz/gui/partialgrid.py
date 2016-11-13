# partialgrid.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Grids for listing details of partial positions on chess database.
"""

import tkinter

from gridsup.datagrid import DataGrid

from ..core.chessrecord import ChessDBrecordPartial
from .partialdisplay import DatabasePartialDisplay, DatabasePartialEdit
from .partialrow import ChessDBrowPartial
from .chessexception import ChessException
from ..core import exporters
from .eventspec import EventSpec, DummyEvent
from .display import Display
from ..core.constants import NAME_DELIMITER


class PartialListGrid(ChessException, DataGrid, Display):

    """A DataGrid for lists of partial positions.

    Subclasses provide navigation and extra methods appropriate to list use.
    
    """

    def __init__(self, parent, ui):
        '''Extend with link to user interface object.

        parent - see superclass
        ui - container for user interface widgets and methods.

        '''
        super(PartialListGrid, self).__init__(parent=parent)
        self.gcanvas.configure(takefocus=tkinter.FALSE)
        self.data.configure(takefocus=tkinter.FALSE)
        self.frame.configure(takefocus=tkinter.FALSE)
        self.hsbar.configure(takefocus=tkinter.FALSE)
        self.vsbar.configure(takefocus=tkinter.FALSE)
        self.ui = ui
        for sequence, function in (
            (EventSpec.tab_traverse_forward,
             self.traverse_forward),
            (EventSpec.tab_traverse_backward,
             self.traverse_backward),
            (EventSpec.tab_traverse_round,
             self.traverse_round),
            ):
            if function:
                function = self.try_event(function)
            self.frame.bind(sequence[0], function)

    def display_selected_item(self, key):
        '''Create display return DatabasePartialDisplay for partial position.'''
        selected = self.get_visible_record(key)
        if selected is None:
            return None
        # Should the Frame containing board and position be created here and
        # passed to DatabasePartialDisplay. (Needs 'import Tkinter' above.)
        # Rather than passing the container where the Frame created by
        # DatabasePartialDisplay is to be put.
        partial = self.make_display_widget(selected)
        #partial.set_position(reset_undo=True)
        self.ui.add_partial_position_to_display(partial)
        self.ui.partial_items.increment_object_count(key)
        self.ui.partial_items.set_itemmap(partial, key)
        self.set_properties(key)
        return partial

    def make_display_widget(self, sourceobject):
        """Return a DatabasePartialDisplay for sourceobject."""
        partial = DatabasePartialDisplay(
            master=self.ui.view_partials_pw,
            ui=self.ui,
            items_manager=self.ui.partial_items,
            itemgrid=self.ui.partial_games,
            sourceobject=sourceobject)
        partial.partial.extract_position(sourceobject.get_srvalue())
        partial.partial.process_partial_position()
        return partial
        
    def edit_selected_item(self, key):
        '''Create display return a DatabasePartialEdit for partial position.'''
        selected = self.get_visible_record(key)
        if selected is None:
            return None
        # Should the Frame containing board and position be created here and
        # passed to DatabasePartialEdit. (Which needs 'import Tkinter' above.)
        # Rather than passing the container where the Frame created by
        # DatabasePartialEdit is to be put.
        partial = self.make_edit_widget(selected)
        #partial.set_position(reset_undo=True)
        self.ui.add_partial_position_to_display(partial)
        self.ui.partial_items.increment_object_count(key)
        self.ui.partial_items.set_itemmap(partial, key)
        self.set_properties(key)
        return partial
        
    def make_edit_widget(self, sourceobject):
        """Return a DatabasePartialEdit for sourceobject."""
        partial = DatabasePartialEdit(
            master=self.ui.view_partials_pw,
            ui=self.ui,
            items_manager=self.ui.partial_items,
            itemgrid=self.ui.partial_games,
            sourceobject=sourceobject)
        partial.partial.extract_position(sourceobject.get_srvalue())
        partial.partial.process_partial_position()
        return partial
        
    def set_properties(self, key, dodefaultaction=True):
        """Return True if properties for partial position key set or False."""
        if super(PartialListGrid, self).set_properties(
            key, dodefaultaction=False):
            return True
        if self.ui.partial_items.object_display_count(key):
            self.objects[key].set_background_on_display(
                self.get_row_widgets(key))
            self.set_row_under_pointer_background(key)
            return True
        if dodefaultaction:
            self.objects[key].set_background_normal(self.get_row_widgets(key))
            self.set_row_under_pointer_background(key)
            return True
        return False

    def set_row(self, key, dodefaultaction=True, **kargs):
        """Return row widget for partial position key or None."""
        row = super(PartialListGrid, self).set_row(
            key, dodefaultaction=False, **kargs)
        if row is not None:
            return row
        if key not in self.keys:
            return None
        if self.ui.partial_items.object_display_count(key):
            return self.objects[key].grid_row_on_display(**kargs)
        if dodefaultaction:
            return self.objects[key].grid_row_normal(**kargs)
        else:
            return None

    def select_down(self):
        """Extend to show selection summary in status bar."""
        super(PartialListGrid, self).select_down()
        self.set_selection_text()
        
    def select_up(self):
        """Extend to show selection summary in status bar."""
        super(PartialListGrid, self).select_up()
        self.set_selection_text()
        
    def cancel_selection(self):
        """Extend to clear selection summary from status bar."""
        if self.selection:
            self.ui.statusbar.set_status_text('')
        super(PartialListGrid, self).cancel_selection()

    def launch_delete_record(self, key, modal=True):
        """Create delete dialogue."""
        oldobject = ChessDBrecordPartial()
        oldobject.load_record(
            (self.objects[key].key.pack(), self.objects[key].srvalue))
        self.create_delete_dialog(
            self.objects[key],
            oldobject,
            modal,
            title='Delete Partial Position')

    def launch_edit_record(self, key, modal=True):
        """Create edit dialogue."""
        self.create_edit_dialog(
            self.objects[key],
            ChessDBrecordPartial(),
            ChessDBrecordPartial(),
            False,
            modal,
            title='Edit Partial Position')

    def launch_edit_show_record(self, key, modal=True):
        """Create edit dialogue including reference copy of original."""
        self.create_edit_dialog(
            self.objects[key],
            ChessDBrecordPartial(),
            ChessDBrecordPartial(),
            True,
            modal,
            title='Edit Partial Position')

    def launch_insert_new_record(self, modal=True):
        """Create insert dialogue."""
        newobject = ChessDBrecordPartial()
        instance = self.datasource.new_row()
        instance.srvalue = repr(NAME_DELIMITER)
        self.create_edit_dialog(
            instance,
            newobject,
            None,
            False,
            modal,
            title='New Partial Position')

    def launch_show_record(self, key, modal=True):
        """Create show dialogue."""
        oldobject = ChessDBrecordPartial()
        oldobject.load_record(
            (self.objects[key].key.pack(), self.objects[key].srvalue))
        self.create_show_dialog(
            self.objects[key],
            oldobject,
            modal,
            title='Show Partial Position')
        
    def create_edit_dialog(
        self, instance, newobject, oldobject, showinitial, modal, title=''):
        """Extend to do chess initialization"""
        for x in (newobject, oldobject):
            if x:
                x.load_record((instance.key.pack(), instance.srvalue))
        super(PartialListGrid, self).create_edit_dialog(
            instance, newobject, oldobject, showinitial, modal, title=title)

    def fill_view(
        self,
        currentkey=None,
        down=True,
        topstart=True,
        exclude=True,
        ):
        """Delegate to superclass if database is open otherwise do nothing."""

        # Intend to put this in superclass but must treat the DataClient objects
        # being scrolled as a database to do this properly.  Do this when these
        # objects have been given a database interface used when the database
        # is not open.  (One problem is how to deal with indexes.)

        # Used to deal with temporary closure of database to do Imports of games
        # from PGN files; which can take many hours.
        
        if self.get_database() is not None:
            super(PartialListGrid, self).fill_view(
                currentkey=currentkey,
                down=down,
                topstart=topstart,
                exclude=exclude,
                )

    def load_new_index(self):
        """Delegate to superclass if database is open otherwise do nothing."""

        # Intend to put this in superclass but must treat the DataClient objects
        # being scrolled as a database to do this properly.  Do this when these
        # objects have been given a database interface used when the database
        # is not open.  (One problem is how to deal with indexes.)

        # Used to deal with temporary closure of database to do Imports of games
        # from PGN files; which can take many hours.
        
        if self.get_database() is not None:
            super(PartialListGrid, self).load_new_index()

    def load_new_partial_key(self, key):
        """Delegate to superclass if database is open otherwise do nothing."""

        # Intend to put this in superclass but must treat the DataClient objects
        # being scrolled as a database to do this properly.  Do this when these
        # objects have been given a database interface used when the database
        # is not open.  (One problem is how to deal with indexes.)

        # Used to deal with temporary closure of database to do Imports of games
        # from PGN files; which can take many hours.
        
        if self.get_database() is not None:
            super(PartialListGrid, self).load_new_partial_key(key)

    def on_configure_canvas(self, event=None):
        """Delegate to superclass if database is open otherwise do nothing."""

        # Intend to put this in superclass but must treat the DataClient objects
        # being scrolled as a database to do this properly.  Do this when these
        # objects have been given a database interface used when the database
        # is not open.  (One problem is how to deal with indexes.)

        # Used to deal with temporary closure of database to do Imports of games
        # from PGN files; which can take many hours.
        
        if self.get_database() is not None:
            super(PartialListGrid, self).on_configure_canvas(event=event)

    def on_data_change(self, instance):
        """Delegate to superclass if database is open otherwise do nothing."""

        # Intend to put this in superclass but must treat the DataClient objects
        # being scrolled as a database to do this properly.  Do this when these
        # objects have been given a database interface used when the database
        # is not open.  (One problem is how to deal with indexes.)

        # Used to deal with temporary closure of database to do Imports of games
        # from PGN files; which can take many hours.
        
        if self.get_database() is not None:
            super(PartialListGrid, self).on_data_change(instance)

    def add_navigation_to_popup(self):
        '''Add 'Navigation' entry to popup menu if not already present.'''

        # Cannot see a way of asking 'Does entry exist?' other than:
        try:
            self.menupopup.index('Navigation')
        except:
            self.menupopup_navigation = tkinter.Menu(
                master=self.menupopup, tearoff=False)
            self.menupopup.add_cascade(
                label='Navigation', menu=self.menupopup_navigation)

    def add_navigation_to_popup_no_row(self):
        '''Add 'Navigation' entry to popup menu if not already present.'''

        # Cannot see a way of asking 'Does entry exist?' other than:
        try:
            self.menupopupnorow.index('Navigation')
        except:
            self.menupopup_navigation_no_row = tkinter.Menu(
                master=self.menupopupnorow, tearoff=False)
            self.menupopupnorow.add_cascade(
                label='Navigation', menu=self.menupopup_navigation_no_row)

    def traverse_backward(self, event=None):
        """Give focus to previous widget type in traversal order."""
        self.ui.give_focus_backward(self)
        return 'break'

    def traverse_forward(self, event=None):
        """Give focus to next widget type in traversal order."""
        self.ui.give_focus_forward(self)
        return 'break'

    def traverse_round(self, event=None):
        """Give focus to next widget within active item in traversal order."""
        return 'break'

    def set_focus(self):
        """Give focus to this widget."""
        self.frame.focus_set()
        if self.ui.single_view:
            self.ui.show_just_panedwindow_with_focus(self.frame)

    def is_payload_available(self):
        """Return True if grid is connected to a database."""
        ds = self.get_data_source()
        if ds is None:
            return False
        if ds.get_database() is None:

            # Avoid exception scrolling visible grid not connected to database.
            # Make still just be hack to cope with user interface activity
            # while importing data.
            self.clear_grid_keys()

            return False
        return True

    def export_partial(self, event=None):
        """Export selected partial position definitions."""
        exporters.export_grid_positions(
            self,
            self.ui.get_export_filename('Partial Positions', pgn=False))

    def focus_set_frame(self, event=None):
        """Adjust widget which is losing focus then delegate to superclass."""
        self.ui.set_bindings_on_item_losing_focus_by_pointer_click()
        super().focus_set_frame(event=event)

    def bind_for_widget_without_focus(self):
        """Return True if this item has the focus about to be lost."""
        if self.get_frame().focus_displayof() != self.get_frame():
            return False

        # Nothing to do on losing focus.
        return True
        
    def get_top_widget(self):
        """Return topmost widget for game display.

        The topmost widget is put in a container widget in some way

        """
        # Superclass DataGrid.get_frame() method returns the relevant widget.
        # Name, get_top_widget, is compatible with Game and Partial names.
        return self.get_frame()
        

class PartialGrid(PartialListGrid):

    """Customized PartialListGrid for list of partial positions on database.
    """

    def __init__(self, ui):
        '''Extend with definition and bindings for partial positions on grid.

        ui - container for user interface widgets and methods.

        '''
        super(PartialGrid, self).__init__(ui.partials_pw, ui)
        self.make_header(ChessDBrowPartial.header_specification)
        self.__bind_on()
        for function, accelerator in (
            (self.display_partial_position_from_popup,
             EventSpec.display_partial_from_partial_grid),
            (self.edit_partial_position_from_popup,
             EventSpec.edit_partial_from_partial_grid),
            (self.export_partial,
             EventSpec.export_from_partial_grid),
            ):
            self.menupopup.add_command(
                label=accelerator[1],
                command=self.try_command(function, self.menupopup),
                accelerator=accelerator[2])
        self.add_navigation_to_popup()
        self.add_navigation_to_popup_no_row()
        for function, accelerator in (
            (self.set_focus_position_grid,
             EventSpec.partial_grid_to_position_grid),
            (self.set_focus_gamepanel_item_command,
             EventSpec.partial_grid_to_active_game),
            (self.set_focus_game_grid,
             EventSpec.partial_grid_to_game_grid),
            (self.set_focus_repertoire_grid,
             EventSpec.partial_grid_to_repertoire_grid),
            (self.set_focus_repertoirepanel_item_command,
             EventSpec.partial_grid_to_active_repertoire),
            (self.set_focus_repertoire_game_grid,
             EventSpec.partial_grid_to_repertoire_game_grid),
            (self.set_focus_partialpanel_item_command,
             EventSpec.partial_grid_to_active_partial),
            (self.set_focus_partial_game_grid,
             EventSpec.partial_grid_to_partial_game_grid),
            (self.set_focus_selection_rule_grid,
             EventSpec.partial_grid_to_selection_rule_grid),
            (self.set_focus_selectionpanel_item_command,
             EventSpec.partial_grid_to_active_selection_rule),
            ):
            for m in (self.menupopup_navigation,
                      self.menupopup_navigation_no_row):
                m.add_command(
                    label=accelerator[1],
                    command=self.try_command(function, m),
                    accelerator=accelerator[2])

    def bind_off(self):
        """Disable all bindings."""
        super(PartialGrid, self).bind_off()
        for sequence, function in (
            (EventSpec.partial_grid_to_active_partial, ''),
            (EventSpec.partial_grid_to_partial_game_grid, ''),
            (EventSpec.partial_grid_to_repertoire_grid, ''),
            (EventSpec.partial_grid_to_active_repertoire, ''),
            (EventSpec.partial_grid_to_repertoire_game_grid, ''),
            (EventSpec.partial_grid_to_position_grid, ''),
            (EventSpec.partial_grid_to_active_game,
             self.set_focus_gamepanel_item),
            (EventSpec.partial_grid_to_game_grid, ''),
            (EventSpec.partial_grid_to_selection_rule_grid, ''),
            (EventSpec.partial_grid_to_active_selection_rule, ''),
            (EventSpec.display_partial_from_partial_grid, ''),
            (EventSpec.edit_partial_from_partial_grid, ''),
            (EventSpec.export_from_partial_grid, ''),
            ):
            if function:
                function = self.try_event(function)
            self.frame.bind(sequence[0], function)

    def bind_on(self):
        """Enable all bindings."""
        super(PartialGrid, self).bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Enable all bindings."""
        for sequence, function in (
            (EventSpec.partial_grid_to_active_partial,
             self.set_focus_partialpanel_item),
            (EventSpec.partial_grid_to_partial_game_grid,
             self.set_focus_partial_game_grid),
            (EventSpec.partial_grid_to_repertoire_grid,
             self.set_focus_repertoire_grid),
            (EventSpec.partial_grid_to_active_repertoire,
             self.set_focus_repertoirepanel_item),
            (EventSpec.partial_grid_to_repertoire_game_grid,
             self.set_focus_repertoire_game_grid),
            (EventSpec.partial_grid_to_position_grid,
             self.set_focus_position_grid),
            (EventSpec.partial_grid_to_active_game,
             self.set_focus_gamepanel_item),
            (EventSpec.partial_grid_to_game_grid,
             self.set_focus_game_grid),
            (EventSpec.partial_grid_to_selection_rule_grid,
             self.set_focus_selection_rule_grid),
            (EventSpec.partial_grid_to_active_selection_rule,
             self.set_focus_selectionpanel_item),
            (EventSpec.display_partial_from_partial_grid,
             self.display_partial_position),
            (EventSpec.edit_partial_from_partial_grid,
             self.edit_partial_position),
            (EventSpec.export_from_partial_grid,
             self.export_partial),
            ):
            if function:
                function = self.try_event(function)
            self.frame.bind(sequence[0], function)

    def display_partial_position(self, event=None):
        """Display partial position and cancel selection.

        Call _display_partial_position after idle tasks to allow message display

        """
        self._set_find_partial_name_games(self.selection[0])
        self.frame.after_idle(
            self.try_command(self._display_partial_position, self.frame))

    def display_partial_position_from_popup(self, event=None):
        """Display partial position selected by pointer.

        Call _display_partial_position after idle tasks to allow message display

        """
        self._set_find_partial_name_games(self.pointer_popup_selection)
        self.frame.after_idle(
            self.try_command(
                self._display_partial_position_from_popup, self.frame))

    def _display_partial_position(self):
        """Display partial position and cancel selection.

        Call from display_partial_position only.

        """
        self.display_selected_item(self.get_visible_selected_key())
        self.cancel_selection()

    def _display_partial_position_from_popup(self):
        """Display partial position selected by pointer.

        Call from display_partial_position_from_popup only.

        """
        self.display_selected_item(self.pointer_popup_selection)

    def edit_partial_position(self, event=None):
        """Display partial position allow editing and cancel selection.

        Call _edit_partial_position after idle tasks to allow message display

        """
        self._set_find_partial_name_games(self.selection[0])
        self.frame.after_idle(
            self.try_command(self._edit_partial_position, self.frame))

    def edit_partial_position_from_popup(self, event=None):
        """Display partial position with editing allowed selected by pointer.

        Call _edit_partial_position after idle tasks to allow message display

        """
        self._set_find_partial_name_games(self.pointer_popup_selection)
        self.frame.after_idle(
            self.try_command(
                self._edit_partial_position_from_popup, self.frame))

    def _edit_partial_position(self):
        """Display partial position allow editing and cancel selection.

        Call from edit_partial_position only.

        """
        self.edit_selected_item(self.get_visible_selected_key())
        self.cancel_selection()

    def _edit_partial_position_from_popup(self):
        """Display partial position with editing allowed selected by pointer.

        Call from edit_partial_position_from_popup only.

        """
        self.edit_selected_item(self.pointer_popup_selection)

    def _set_find_partial_name_games(self, key):
        """Set status text to active partial position name."""
        if self.ui.partial_items.count_items_in_stack():
            # do search at this time only if no partial positions displayed
            return
        self.ui.statusbar.set_status_text(
            ''.join(
                ('Please wait while finding games for partial position ',
                 self.objects[key].value.get_name_text(),
                 )))
        
    def on_partial_change(self, instance):
        # may turn out to be just to catch datasource is None
        if self.get_data_source() is None:
            return
        super(PartialGrid, self).on_data_change(instance)

    def set_selection_text(self):
        """Set status bar to display partial position name and piecss."""
        if self.selection:
            p = self.objects[self.selection[0]].value
            self.ui.statusbar.set_status_text(
                ''.join(
                    (p.get_name_text(),
                     '   (',
                     p.get_position_text(delimiter=' '),
                     ')')))
        else:
            self.ui.statusbar.set_status_text('')

    def is_visible(self):
        """Return True if list of partial positions is displayed."""
        return str(self.get_frame()) in self.ui.partials_pw.panes()

    def make_display_widget(self, sourceobject):
        """Return a DatabasePartialDisplay for sourceobject."""
        partial = super().make_display_widget(sourceobject)
        partial.set_position(reset_undo=True)
        return partial
        
    def make_edit_widget(self, sourceobject):
        """Return a DatabasePartialEdit for sourceobject."""
        partial = super().make_edit_widget(sourceobject)
        partial.set_position(reset_undo=True)
        return partial

    def focus_set_frame(self, event=None):
        """Delegate to superclass then set toolbar widget states."""
        super().focus_set_frame(event=event)
        self.ui.set_toolbarframe_normal(
            self.ui.move_to_partial, self.ui.filter_partial)

    def set_selection(self, key):
        """Hack to fix edge case when inserting records using apsw or sqlite3.
        
        Workaround a KeyError exception when a record is inserted while a grid
        keyed by a secondary index with only one key value in the index is on
        display.
        
        """
        try:
            super().set_selection(key)
        except KeyError:
            tkinter.messagebox.showinfo(
                title='Insert Partial Position Workaround',
                message=''.join(
                    ('All records have same name on this display.\n\nThe new ',
                     'record has been inserted but you need to Hide, and then ',
                     'Show, the display to see the record in the list.',
                     )))
