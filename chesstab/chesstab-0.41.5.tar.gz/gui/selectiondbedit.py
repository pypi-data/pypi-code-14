# selectiondbedit.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Customise edit dialogue to edit or insert game selection rule record.
"""

from basesup.tools import dialogues

from .dataedit import DataEdit
from .chessexception import ChessException
from .selectiondisplay import DialogueSelectionDisplay, DialogueSelectionEdit


class ChessDBeditSelection(ChessException, DataEdit):
    """Dialog to edit a game selection rule on, or insert one into, database.

    The game selection rule is in it's own Toplevel widget.

    """

    def __init__(self, newobject, parent, oldobject, showinitial=True, ui=None):
        """Extend and create dialogue to edit or insert selection rule."""
        if oldobject:
            title = ':  '.join((
                'Edit Selection Rule',
                oldobject.value._description_string))
        else:
            title = 'Insert Selection Rule'
            showinitial = False
        self.__title = title.split(':')[0]
        if showinitial:
            showinitial = DialogueSelectionDisplay(master=parent, ui=ui)
            if ui is not None:
                ui.selections_in_toplevels.add(showinitial)
            if oldobject.database is not None:
                showinitial.selection_rule.extract_selection_rule(
                    oldobject.get_srvalue())
            else:
                showinitial.selection_rule.extract_selection_rule(
                    oldobject.get_srvalue_as_str())
            showinitial.selection_rule.process_selection_rule()
            showinitial.set_selection_rule()
        newview = DialogueSelectionEdit(master=parent, ui=ui)
        if ui is not None:
            ui.selections_in_toplevels.add(newview)
        if newobject.database is not None:
            newview.selection_rule.extract_selection_rule(
                newobject.get_srvalue())
        else:
            newview.selection_rule.extract_selection_rule(
                newobject.get_srvalue_as_str())
        newview.selection_rule.process_selection_rule()
        newview.set_selection_rule()
        super(ChessDBeditSelection, self).__init__(
            newobject,
            parent,
            oldobject,
            newview,
            title,
            oldview=showinitial,
            )

        # Bind only to newview.score because it alone takes focus.
        self.bind_buttons_to_widget(newview.score)

        self.ui = ui
        
    def dialog_ok(self):
        """Update record and return update action response (True for updated).

        Check that database is open and is same one as update action was
        started.

        """
        if self.ui.database is None:
            self.status.configure(
                text='Cannot update because not connected to a database')
            if self.ok:
                self.ok.destroy()
                self.ok = None
            self.blockchange = True
            return False
        self.newobject.value.load(
            repr(self.newview.get_name_selection_rule_text()))
        if not self.newobject.value.get_selection_rule_text():
            dialogues.showerror(
                title=self.__title,
                message=''.join(('No game selection rule given.\n\n',
                                 'Name of game selection rule must be first ',
                                 'line, and subsequent lines the rule.',
                                 )))
            return False
        return super(ChessDBeditSelection, self).dialog_ok()

    def tidy_on_destroy(self):
        """Clear up after dialogue destruction."""
        self.ui.selections_in_toplevels.discard(self.oldview)
        self.ui.selections_in_toplevels.discard(self.newview)
        self.ui.base_selections.selection.clear()
