# selectiondbdelete.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Customise delete dialogue to delete game selection rule record.
"""

from .datadelete import DataDelete
from .chessexception import ChessException
from .selectiondisplay import DialogueSelectionDisplay


class ChessDBdeleteSelection(ChessException, DataDelete):
    """Dialog to delete a game selection rule from database.

    The game selection rule is in it's own Toplevel widget.

    """

    def __init__(self, parent, instance, ui=None):
        """Extend and create dialogue widget for deleting selection rule."""
        oldview = DialogueSelectionDisplay(master=parent, ui=ui)
        if ui is not None:
            ui.selections_in_toplevels.add(oldview)
        if instance.database is not None:
            oldview.selection_rule.extract_selection_rule(
                instance.get_srvalue())
        else:
            oldview.selection_rule.extract_selection_rule(
                instance.get_srvalue_as_str())
        oldview.selection_rule.process_selection_rule()
        oldview.set_selection_rule(instance.value)
        super(ChessDBdeleteSelection, self).__init__(
            instance,
            parent,
            oldview,
            ':  '.join((
                'Delete Selection Rule',
                instance.value._description_string)),
            )
        self.bind_buttons_to_widget(oldview.score)
        self.ui = ui
       
    def dialog_ok(self):
        """Delete record and return delete action response (True for deleted).

        Check that database is open and is same one as deletion action was
        started.

        """
        if self.ui.database is None:
            self.status.configure(
                text='Cannot delete because not connected to a database')
            if self.ok:
                self.ok.destroy()
                self.ok = None
            self.blockchange = True
            return False
        return super(ChessDBdeleteSelection, self).dialog_ok()

    def tidy_on_destroy(self):
        """Clear up after dialogue destruction."""
        self.ui.selections_in_toplevels.discard(self.oldview)
        self.ui.base_selections.selection.clear()
