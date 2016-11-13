# partialdisplay.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Widgets to display and edit partial positions.

These four classes display partial positions in the main window: they are used
in the partialgrid module.

The PartialDisplay class binds events to navigate between widgets.

The DatabasePartialDisplay class adds delete record to the PartialDisplay class.

The DatabasePartialInsert class adds insert record to the
DatabasePartialDisplay class but does not bind delete record to any events.

The DatabasePartialEdit class adds edit record to the DatabasePartialDisplay
class but does not bind delete record to any events.

These three classes display partial positions in their own Toplevel widget: they
are used in the partialdbdelete, partialdbedit, and partialdbshow, modules.

The PartialDialogue class binds events to navigate between widgets.

The DialoguePartialDisplay class adds insert and delete record to the
PartialDialogue class.

The DialoguePartialEdit class adds insert and edit record to the PartialDialogue
class.

"""

import tkinter
import tkinter.messagebox

from basesup.tools import dialogues

from gridsup.gui.dataedit import RecordEdit
from gridsup.gui.datadelete import RecordDelete
from gridsup.core.dataclient import DataNotify

from .partial import Partial
from .partialedit import PartialEdit
from ..core.chessrecord import ChessDBrecordPartial
from .chessexception import ChessException
from ..core.constants import NAME_DELIMITER
from .eventspec import EventSpec
from .display import Display


class PartialDisplay(ChessException, Display):
    
    """Manage UI interaction with database for displayed partial position.

    PartialDisplay is a subclass of DataNotify so that modifications to
    the database record outside an instance prevent database update using
    the instance.  This class provides methods to update the database from
    the instance; and to switch to other displayed partial positions.

    Subclasses provide the widget to display the partial position.
    
    """

    binding_labels = tuple(
        [b[1:] for b in (
            EventSpec.partialdisplay_to_position_grid,
            EventSpec.partialdisplay_to_active_game,
            EventSpec.partialdisplay_to_game_grid,
            EventSpec.partialdisplay_to_repertoire_grid,
            EventSpec.partialdisplay_to_active_repertoire,
            EventSpec.partialdisplay_to_repertoire_game_grid,
            EventSpec.partialdisplay_to_partial_grid,
            EventSpec.partialdisplay_to_previous_partial,
            EventSpec.partialdisplay_to_next_partial,
            EventSpec.partialdisplay_to_partial_game_grid,
            EventSpec.partialdisplay_to_selection_rule_grid,
            EventSpec.partialdisplay_to_active_selection_rule,
            EventSpec.tab_traverse_backward,
            EventSpec.tab_traverse_forward,
            )])

    def __init__(self, sourceobject=None, **ka):
        """Extend and link partial position to database.

        sourceobject - link to database.

        """
        super(PartialDisplay, self).__init__(**ka)
        self.blockchange = False
        if self.ui.base_partials.datasource:
            self.set_data_source(self.ui.base_partials.get_data_source())
        self.sourceobject = sourceobject
        self.insertonly = sourceobject is None
        self.recalculate_after_edit = sourceobject

    def _bind_for_board_navigation(self):
        """Set bindings to navigate partial position on pointer click."""
        self.bind_board_pointer_for_board_navigation(True)
        self.bind_score_pointer_for_board_navigation(True)

    def bind_for_widget_navigation(self):
        """Set bindings to give focus to this partial position on pointer click.
        """
        self.bind_score_pointer_for_widget_navigation(True)
        self.bind_board_pointer_for_widget_navigation(True)

    def bind_off(self):
        """Disable all bindings."""
        
        # Replicate structure of __bind_on for deleting bindings.
        for sequence, function in (
            (EventSpec.partialdisplay_to_partial_grid, ''),
            (EventSpec.partialdisplay_to_previous_partial, ''),
            (EventSpec.partialdisplay_to_next_partial, ''),
            (EventSpec.partialdisplay_to_partial_game_grid, ''),
            (EventSpec.partialdisplay_to_repertoire_grid, ''),
            (EventSpec.partialdisplay_to_active_repertoire, ''),
            (EventSpec.partialdisplay_to_repertoire_game_grid, ''),
            (EventSpec.partialdisplay_to_position_grid, ''),
            (EventSpec.partialdisplay_to_active_game, ''),
            (EventSpec.partialdisplay_to_selection_rule_grid, ''),
            (EventSpec.partialdisplay_to_active_selection_rule, ''),
            (EventSpec.partialdisplay_to_game_grid, ''),
            (EventSpec.export_from_partialdisplay, ''),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    # This method exists because the bindings cannot be done until all __init__
    # methods in superclasses have been called.
    def initialize_bindings(self):
        """Initialize all bindings."""
        self.__bind_on()
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
            self.score.bind(sequence[0], function)

    def bind_on(self):
        """Enable all bindings."""
        self.__bind_on()

    def __bind_on(self):
        """Enable all bindings."""

        # Same bindings in initialize_bindings() and bind_on() in this class.
        for sequence, function in (
            ('<Control-ButtonPress-1>', ''),
            ('<ButtonPress-1>', self.try_event(self.give_focus_to_widget)),
            ('<ButtonPress-3>', self.try_event(self.popup_inactive_menu)),
            ):
            for w in self.board.boardsquares.values():
                w.bind(sequence, function)
            self.score.bind(sequence, function)
        for sequence, function in (
            (EventSpec.partialdisplay_to_partial_grid,
             self.set_focus_partial_grid),
            (EventSpec.partialdisplay_to_previous_partial,
             self.prior_item),
            (EventSpec.partialdisplay_to_next_partial,
             self.next_item),
            (EventSpec.partialdisplay_to_partial_game_grid,
             self.set_focus_partial_game_grid),
            (EventSpec.partialdisplay_to_repertoire_grid,
             self.set_focus_repertoire_grid),
            (EventSpec.partialdisplay_to_active_repertoire,
             self.set_focus_repertoirepanel_item),
            (EventSpec.partialdisplay_to_repertoire_game_grid,
             self.set_focus_repertoire_game_grid),
            (EventSpec.partialdisplay_to_position_grid,
             self.set_focus_position_grid),
            (EventSpec.partialdisplay_to_active_game,
             self.set_focus_gamepanel_item),
            (EventSpec.partialdisplay_to_selection_rule_grid,
             self.set_focus_selection_rule_grid),
            (EventSpec.partialdisplay_to_active_selection_rule,
             self.set_focus_selectionpanel_item),
            (EventSpec.partialdisplay_to_game_grid,
             self.set_focus_game_grid),
            (EventSpec.export_from_partialdisplay,
             self.export_partial),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    def _cycle_item(self, prior=False):
        """Select next partial position on display."""
        items = self.ui.partial_items
        losefocus = items.active_item
        losefocus.bind_for_widget_navigation()
        items.cycle_active_item(prior=prior)
        self.ui.configure_partial_grid()
        gainfocus = items.active_item
        gainfocus.set_game_list()
        gainfocus._bind_for_board_navigation()
        gainfocus.takefocus_widget.focus_set()
        gainfocus.set_statusbar_text()

    def give_focus_to_widget(self, event=None):
        """Select partial position on display by mouse click."""
        self.ui.set_bindings_on_item_losing_focus_by_pointer_click()
        losefocus, gainfocus = self.ui.partial_items.give_focus_to_widget(
            event.widget)
        if losefocus is not gainfocus:
            self.ui.configure_partial_grid()
            self.score.after(
                0, func=self.try_command(self.ui._set_partial_name, self.score))
            self.score.after(
                0,
                func=self.try_command(gainfocus.set_game_list, self.score))
        return 'break'

    def delete_item_view(self, event=None):
        """Remove partial position item from screen."""
        self.ui.delete_position_view(self)

    def insert_position_database(self, event=None):
        """Add partial position to database."""
        if self.ui.partial_items.active_item is None:
            dialogues.showerror(
                title='Insert Partial Position',
                message='No active partial position to insert into database.')
            return
        if self.ui.database is None:
            dialogues.showinfo(
                title='Insert Partial Position',
                message='Cannot add partial position:\n\nNo database open.')
            return

        datasource = self.ui.base_partials.get_data_source()
        if datasource is None:
            dialogues.showerror(
                title='Insert Partial Position',
                message=''.join(('Cannot add partial position:\n\n',
                                 'Partial position list hidden.')))
            return
        updater = ChessDBrecordPartial()
        if not updater.value.extract_position(self.get_name_position_text()):
            dialogues.showerror(
                title='Insert Partial Position',
                message=''.join(('Name of partial position must be first ',
                                 'line, and subsequent lines a valid partial ',
                                 'position.',
                                 )))
            return
        updater.value.process_partial_position()
        if not updater.value.is_position():
            dialogues.showerror(
                title='Insert Partial Position',
                message=''.join(('Name of partial position must be first ',
                                 'line, and subsequent lines a valid partial ',
                                 'position.',
                                 )))
            return

        # Name of partial position must not be duplicated.
        # At least on Sqlite3.
        
        if tkinter.messagebox.YES != dialogues.askquestion(
            title='Insert Partial Position',
            message=''.join((
                'Confirm request to add partial position ',
                'to database'))):
            dialogues.showinfo(
                title='Insert Partial Position',
                message='Add partial position to database abandonned.')
            return
        editor = RecordEdit(updater, None)
        editor.set_data_source(datasource, editor.on_data_change)
        updater.set_database(editor.get_data_source().dbhome)
        updater.key.recno = 0
        editor.put()
        dialogues.showinfo(
            title='Insert Partial Position',
            message=''.join(('Partial position "',
                             updater.value.get_name_text(),
                             '" added to database.')))
        
    def next_item(self, event=None):
        """Select next partial position display.

        Call _next_position after 1 millisecond to allow message display

        """
        if self.ui.partial_items.count_items_in_stack() > 1:
            self.ui._set_find_partial_name_games(0)
            self.score.after(
                1, func=self.try_command(self._next_position, self.score))

    def _next_position(self):
        """Generate next partial position display.

        Call from next_item only.

        """
        self._cycle_item(prior=False)

    def on_game_change(self, instance):
        """Recalculate list of games for partial position after game update.

        instance is ignored: it is assumed a recalculation is needed.

        """
        if self.sourceobject is not None:
            self._calculate_partial_position_games()

    def on_partial_change(self, instance):
        """Prevent update from self if instance refers to same record."""
        if self.sourceobject is not None:
            if (instance.key == self.sourceobject.key and
                self.datasource.dbname == self.sourceobject.dbname and
                self.datasource.dbset == self.sourceobject.dbset):
                self.blockchange = True
            if self is self.ui.partial_items.active_item:
                self._calculate_partial_position_games()

    def prior_item(self, event=None):
        """Select previous partial position display.

        Call _prior_position after 1 millisecond to allow message display

        """
        if self.ui.partial_items.count_items_in_stack() > 1:
            self.ui._set_find_partial_name_games(-2)
            self.score.after(
                1, func=self.try_command(self._prior_position, self.score))

    def _prior_position(self):
        """Generate previous partial position display.

        Call from prior_item only.

        """
        self._cycle_item(prior=True)

    def set_insert_or_delete(self):
        """Convert edit display to insert display.

        Partial positions displayed for editing from a database are not closed
        if the database is closed.  They are converted to insert displays and
        can be used to add new records to databases opened later.
        
        """
        self.sourceobject = None

    def get_text_for_statusbar(self):
        """"""
        return ''.join(
            ('Please wait while finding games for partial position ',
             self.partial.get_name_text(),
             ))

    def get_selection_text_for_statusbar(self):
        """"""
        return self.partial.get_name_text()
        
    def bind_toplevel_navigation(self):
        """Set bindings for popup menu for PartialDisplay instance."""
        navigation_map = {
            EventSpec.partialdisplay_to_position_grid[1]:
            self.set_focus_position_grid,
            EventSpec.partialdisplay_to_active_game[1]:
            self.set_focus_gamepanel_item_command,
            EventSpec.partialdisplay_to_game_grid[1]:
            self.set_focus_game_grid,
            EventSpec.partialdisplay_to_repertoire_grid[1]:
            self.set_focus_repertoire_grid,
            EventSpec.partialdisplay_to_active_repertoire[1]:
            self.set_focus_repertoirepanel_item_command,
            EventSpec.partialdisplay_to_repertoire_game_grid[1]:
            self.set_focus_repertoire_game_grid,
            EventSpec.partialdisplay_to_partial_grid[1]:
            self.set_focus_partial_grid,
            EventSpec.partialdisplay_to_partial_game_grid[1]:
            self.set_focus_partial_game_grid,
            EventSpec.partialdisplay_to_selection_rule_grid[1]:
            self.set_focus_selection_rule_grid,
            EventSpec.partialdisplay_to_active_selection_rule[1]:
            self.set_focus_selectionpanel_item_command,
            EventSpec.tab_traverse_backward[1]:
            self.traverse_backward,
            EventSpec.tab_traverse_forward[1]:
            self.traverse_forward,
            }
        for nm, widget in (
            ({EventSpec.partialdisplay_to_previous_partial[1]: self.prior_item,
              EventSpec.partialdisplay_to_next_partial[1]: self.next_item,
              },
             self),
            ):
            nm.update(navigation_map)
            widget.add_navigation_to_viewmode_popup(
                bindings=nm, order=self.binding_labels)

    def set_game_list_after(self):
        """"""
        self.panel.after(
            0, func=self.try_command(self.ui._set_partial_name, self.panel))
        self.panel.after(
            0,
            func=self.try_command(self.set_game_list, self.panel))

    def traverse_backward(self, event=None):
        """Give focus to previous widget type in traversal order."""
        self.ui.give_focus_backward(self.ui.partial_items)
        return 'break'

    def traverse_forward(self, event=None):
        """Give focus to next widget type in traversal order."""
        self.ui.give_focus_forward(self.ui.partial_items)
        return 'break'

    def traverse_round(self, event=None):
        """Give focus to next widget within active item in traversal order."""
        return 'break'

    def _calculate_partial_position_games(self):
        """"""
        p = self.ui.partial_games
        if len(p.keys):
            key = p.keys[0]
        else:
            key = None
        p.close_client_cursor()
        p.datasource.get_partial_position_games(
            self.get_partial_key_partial_position(),
            self.sourceobject)
        p.fill_view(currentkey=key, exclude=False)


class DatabasePartialDisplay(PartialDisplay, Partial, DataNotify):
    
    """Display partial position from database and allow delete edit and insert.

    Partial provides the widget and PartialDisplay the database interface.
    
    """

    def __init__(self, **ka):
        """Create and display partial position widget.

        See superclasses for argument descriptions.

        """
        super(DatabasePartialDisplay, self).__init__(**ka)
        self.initialize_bindings()

    def bind_off(self):
        """Disable all bindings."""
        super(DatabasePartialDisplay, self).bind_off()
        for sequence, function in (
            (EventSpec.databasepartialdisplay_insert, ''),
            (EventSpec.databasepartialdisplay_delete, ''),
            (EventSpec.databasepartialdisplay_dismiss, ''),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    # This method exists because the bindings cannot be done until all __init__
    # methods in superclasses have been called.
    def initialize_bindings(self):
        """Initialize all bindings."""
        super(DatabasePartialDisplay, self).initialize_bindings()

        # Here because superclass order is PartialDisplay, Partial.
        self.inactive_popup = tkinter.Menu(master=self.score, tearoff=False)

        for function, accelerator in (
            (self.set_focus_panel_item_command,
             EventSpec.databasepartialdisplay_make_active),
            (self.delete_item_view,
             EventSpec.databasepartialdisplay_dismiss_inactive),
            ):
            self.inactive_popup.add_command(
                label=accelerator[1],
                command=self.try_command(function, self.inactive_popup),
                accelerator=accelerator[2])
        self.__bind_on()
        for function, accelerator in (
            (self.delete_item_view,
             EventSpec.databasepartialdisplay_dismiss),
            ):
            self.viewmode_popup.add_command(
                label=accelerator[1],
                command=self.try_command(function, self.viewmode_popup),
                accelerator=accelerator[2])
        for function, accelerator in (
            (self.insert_position_database,
             EventSpec.databasepartialdisplay_insert),
            (self.delete_position_database,
             EventSpec.databasepartialdisplay_delete),
            ):
            self.viewmode_database_popup.add_command(
                label=accelerator[1],
                command=self.try_command(
                    function, self.viewmode_database_popup),
                accelerator=accelerator[2])
        self.bind_toplevel_navigation()

    def bind_on(self):
        """Enable all bindings."""
        super(DatabasePartialDisplay, self).bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Common to bind_on() and initialize_bindings()"""
        for sequence, function in (
            (EventSpec.databasepartialdisplay_insert,
             self.insert_position_database),
            (EventSpec.databasepartialdisplay_delete,
             self.delete_position_database),
            (EventSpec.databasepartialdisplay_dismiss,
             self.delete_item_view),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    def delete_position_database(self, event=None):
        """Remove partial position from database."""
        if self.ui.database is None:
            dialogues.showinfo(
                title='Delete Partial Position',
                message='Cannot delete partial position:\n\nNo database open.')
            return
        datasource = self.ui.base_partials.get_data_source()
        if datasource is None:
            dialogues.showerror(
                title='Delete Partial Position',
                message=''.join(('Cannot delete partial position:\n\n',
                                 'Partial position list hidden.')))
            return
        if self.blockchange:
            dialogues.showinfo(
                title='Delete Partial Position',
                message='\n'.join((
                    'Cannot delete partial position.',
                    'Record has been amended since this copy displayed.')))
            return
        p = self.partial
        if p._state is not None:
            v = self.sourceobject.value
            if (p.get_name_text() != v.get_name_text() or
                p._state != v._state or
                p.get_position_text() != v.get_position_text()):
                dialogues.showinfo(
                    title='Delete Partial Position',
                    message='\n'.join((
                        'Cannot delete partial position.',
                        ' '.join((
                            'Position on display is not same as',
                            'position from record.')))))
                return
        if tkinter.messagebox.YES != dialogues.askquestion(
            title='Delete Partial Position',
            message='Confirm request to delete partial position'):
            return
        editor = RecordDelete(self.sourceobject)
        editor.set_data_source(datasource, editor.on_data_change)
        editor.delete()
        dialogues.showinfo(
            title='Delete Partial Position',
            message=''.join(('Partial position "',
                             self.sourceobject.value.get_name_text(),
                             '" deleted from database.')))


class DatabasePartialInsert(PartialDisplay, PartialEdit, DataNotify):
    
    """Display partial position from database and allow delete and insert.

    PartialEdit provides the widget and PartialDisplay the
    database interface.
    
    """

    def __init__(self, **ka):
        """Create and display partial position widget.

        See superclasses for argument descriptions.

        """
        super().__init__(**ka)
        self.initialize_bindings()

    def bind_off(self):
        """Disable all bindings."""
        super().bind_off()
        for sequence, function in (
            (EventSpec.databasepartialedit_show_game_list, ''),
            (EventSpec.databasepartialedit_insert, ''),
            (EventSpec.databasepartialedit_dismiss, ''),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    # This method exists because the bindings cannot be done until all __init__
    # methods in superclasses have been called.
    def initialize_bindings(self):
        """Initialize all bindings."""
        super().initialize_bindings()

        # Here because superclass order is PartialDisplay, PartialEdit.
        self.inactive_popup = tkinter.Menu(master=self.score, tearoff=False)

        for function, accelerator in (
            (self.set_focus_panel_item_command,
             EventSpec.databasepartialedit_make_active),
            (self.delete_item_view,
             EventSpec.databasepartialedit_dismiss_inactive),
            ):
            self.inactive_popup.add_command(
                label=accelerator[1],
                command=self.try_command(function, self.inactive_popup),
                accelerator=accelerator[2])
        self.__bind_on()
        for function, accelerator in (
            (self.process_and_set_position_list,
             EventSpec.databasepartialedit_show_game_list),
            (self.delete_item_view,
             EventSpec.databasepartialedit_dismiss),
            ):
            self.viewmode_popup.add_command(
                label=accelerator[1],
                command=self.try_command(function, self.viewmode_popup),
                accelerator=accelerator[2])
        for function, accelerator in (
            (self.insert_position_database,
             EventSpec.databasepartialedit_insert),
            ):
            self.viewmode_database_popup.add_command(
                label=accelerator[1],
                command=self.try_command(
                    function, self.viewmode_database_popup),
                accelerator=accelerator[2])
        self.bind_toplevel_navigation()

    def bind_on(self):
        """Enable all bindings."""
        super().bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Common to bind_on() and initialize_bindings()"""
        for sequence, function in (
            (EventSpec.databasepartialedit_show_game_list,
             self.process_and_set_position_list),
            (EventSpec.databasepartialedit_insert,
             self.insert_position_database),
            (EventSpec.databasepartialedit_dismiss,
             self.delete_item_view),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    def process_and_set_position_list(self, event=None):
        """Display games with position matching edited partial position."""
        self.partial.extract_position(
            self.score.get('1.0', tkinter.END), delimiter='\n')
        self.partial.process_partial_position()
        self.set_game_list()
        return 'break'

    def insert_char_to_right(self, char):
        """"""
        r = super().insert_char_to_right(char)
        if r is None:
            return None
        elif r:
            return True
        else:
            self.recalculate_after_edit = None
            return None

    def delete_char_left(self, event):
        """"""
        if not self.current:
            return 'break'
        self.recalculate_after_edit = None
        return super().delete_char_left(event)

    def delete_char_right(self, event):
        """"""
        if not self.current:
            return 'break'
        self.recalculate_after_edit = None
        return super().delete_char_right(event)


class DatabasePartialEdit(DatabasePartialInsert):
    
    """Display partial position from database and allow delete edit and insert.

    PartialEdit provides the widget and PartialDisplay the
    database interface.
    
    """

    def bind_off(self):
        """Disable all bindings."""
        super().bind_off()
        for sequence, function in (
            (EventSpec.databasepartialedit_update, ''),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    # This method exists because the bindings cannot be done until all __init__
    # methods in superclasses have been called.
    def initialize_bindings(self):
        """Initialize all bindings."""
        super().initialize_bindings()
        for function, accelerator in (
            (self.update_position_database,
             EventSpec.databasepartialedit_update),
            ):
            self.viewmode_database_popup.add_command(
                label=accelerator[1],
                command=self.try_command(
                    function, self.viewmode_database_popup),
                accelerator=accelerator[2])
        self.bind_toplevel_navigation()

    def bind_on(self):
        """Enable all bindings."""
        super().bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Common to bind_on() and initialize_bindings()"""
        for sequence, function in (
            (EventSpec.databasepartialedit_update,
             self.update_position_database),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    def update_position_database(self, event=None):
        """Modify existing partial position record."""
        if self.ui.database is None:
            dialogues.showinfo(
                title='Edit Partial Position',
                message='Cannot edit partial position:\n\nNo database open.')
            return
        datasource = self.ui.base_partials.get_data_source()
        if datasource is None:
            dialogues.showerror(
                title='Edit Partial Position',
                message=''.join(('Cannot edit partial position:\n\n',
                                 'Partial position list hidden.')))
            return
        if self.sourceobject is None:
            dialogues.showinfo(
                title='Edit Partial Position',
                message=''.join(('The partial position to edit has not ',
                                 'been given.\n\nProbably because database ',
                                 'has been closed and opened since this copy ',
                                 'was displayed.')))
            return
        if self.blockchange:
            dialogues.showinfo(
                title='Edit Partial Position',
                message='\n'.join((
                    'Cannot edit partial position.',
                    'It has been amended since this copy was displayed.')))
            return
        original = ChessDBrecordPartial()
        original.load_record(
            (self.sourceobject.key.recno,
             self.sourceobject.srvalue))

        # is it better to use DataClient directly?
        # Then original would not be used. Instead DataSource.new_row
        # gets record keyed by sourceobject and update is used to edit this.
        updater = ChessDBrecordPartial()
        if not updater.value.extract_position(self.get_name_position_text()):
            dialogues.showerror(
                title='Edit Partial Position',
                message=''.join(('Name of partial position must be first ',
                                 'line, and subsequent lines a valid partial ',
                                 'position.',
                                 )))
            return
        updater.value.process_partial_position()
        if not updater.value.is_position():
            dialogues.showerror(
                title='Edit Partial Position',
                message=''.join(('Name of partial position must be first ',
                                 'line, and subsequent lines a valid partial ',
                                 'position.',
                                 )))
            return
        if tkinter.messagebox.YES != dialogues.askquestion(
            title='Edit Partial Position',
            message=''.join((
                'Confirm request to edit partial position named:\n\n',
                updater.value.get_name_text(),
                '\n\non database.',))):
            dialogues.showinfo(
                title='Edit Partial Position',
                message='Edit partial position on database abandonned.')
            return
        editor = RecordEdit(updater, original)
        editor.set_data_source(datasource, editor.on_data_change)
        updater.set_database(editor.get_data_source().dbhome)
        original.set_database(editor.get_data_source().dbhome)
        updater.key.recno = original.key.recno
        editor.edit()
        if self is self.ui.partial_items.active_item:
            newkey = self.ui.partial_items.adjust_edited_item(updater)
            if newkey:
                self.ui.base_partials.set_properties(newkey)
        dialogues.showinfo(
            title='Edit Partial Position',
            message=''.join(('Partial position "',
                             updater.value.get_name_text(),
                             '" amended on database.')))


class PartialDialogue(ChessException):
    
    """Manage UI interaction with database for displayed partial position.

    Subclasses provide the widget to display the partial position.
    
    """

    # Formally the same as GameDialogue in gamedisplay module.
    # Follow whatever style of assignment is used there if this binding_labels
    # needs to be non-empty.
    binding_labels = tuple()

    def initialize_bindings(self):
        """Enable all bindings."""
        self.bind_board_pointer_for_board_navigation(True)
        self.bind_score_pointer_for_board_navigation(True)
        self.bind_toplevel_navigation()
        
    def bind_toplevel_navigation(self):
        """Set bindings for popup menu for PartialDialogue instance."""

        # Formally the same as GameDialogue in gamedisplay module.
        # The effect is add no bindings to an empty bindings map.
        navigation_map = {}
        for nm, widget in (
            ({},
             self),
            ):
            nm.update(navigation_map)
            widget.add_navigation_to_viewmode_popup(
                bindings=nm, order=self.binding_labels)


class DialoguePartialDisplay(Partial, PartialDialogue):
    
    """Display a partial position from a database allowing delete and insert.
    """

    def __init__(self, **ka):
        """Extend and link partial position to database."""
        super(DialoguePartialDisplay, self).__init__(**ka)
        self.initialize_bindings()
        
    def set_game_list(self):
        """Display list of records in grid.

        Called after each navigation event on a partial position including
        switching from one partial position to another.
        
        """
        # PartialScore.set_game_list() expects instance to have itemgrid
        # attribute bound to a DataGrid subclass instance, but
        # DialoguePartialDisplay instance can live without this being present.
        # It may be more appropriate to override set_game_list to do nothing so
        # there is a way of editing or inserting a partial position without
        # tracking games containing the same positions.
        try:
            super().set_game_list()
        except AttributeError:
            if self.itemgrid is not None:
                raise


class DialoguePartialEdit(PartialEdit, PartialDialogue):
    
    """Display a partial position from a database allowing edit and insert.
    """

    def __init__(self, **ka):
        """Extend and link partial position to database."""
        super(DialoguePartialEdit, self).__init__(**ka)
        self.initialize_bindings()
        
    def set_game_list(self):
        """Display list of records in grid.

        Called after each navigation event on a partial position including
        switching from one partial position to another.
        
        """
        # PartialScore.set_game_list() expects instance to have itemgrid
        # attribute bound to a DataGrid subclass instance, but
        # DialoguePartialEdit instance can live without this being present.
        # It may be more appropriate to override set_game_list to do nothing so
        # there is a way of editing or inserting a partial position without
        # tracking games containing the same positions.
        try:
            super().set_game_list()
        except AttributeError:
            if self.itemgrid is not None:
                raise
