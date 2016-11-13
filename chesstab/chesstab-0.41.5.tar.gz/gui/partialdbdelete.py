# partialdbdelete.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Customise delete dialogue to delete partial position record.
"""

from .datadelete import DataDelete
from .chessexception import ChessException
from .partialdisplay import DialoguePartialDisplay


class ChessDBdeletePartial(ChessException, DataDelete):
    """Dialog to delete a partial position from database.

    The partial position is in it's own Toplevel widget.

    """

    def __init__(self, parent, instance, ui=None):
        """Extend and create dialogue widget for deleting partial position."""
        oldview = DialoguePartialDisplay(master=parent, ui=ui)
        if ui is not None:
            ui.partials_in_toplevels.add(oldview)
        if instance.database is not None:
            oldview.partial.extract_position(instance.get_srvalue())
        else:
            oldview.partial.extract_position(instance.get_srvalue_as_str())
        oldview.partial.process_partial_position()
        oldview.set_position(instance.value)
        super(ChessDBdeletePartial, self).__init__(
            instance,
            parent,
            oldview,
            ':  '.join((
                'Delete Partial Position',
                instance.value.get_name_text())),
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
        return super(ChessDBdeletePartial, self).dialog_ok()

    def tidy_on_destroy(self):
        """Clear up after dialogue destruction."""
        self.ui.partials_in_toplevels.discard(self.oldview)
        self.ui.base_partials.selection.clear()
