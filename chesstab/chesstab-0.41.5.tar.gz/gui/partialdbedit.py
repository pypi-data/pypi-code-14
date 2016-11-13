# partialdbedit.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Customise edit dialogue to edit or insert partial position record.
"""

from basesup.tools import dialogues

from .dataedit import DataEdit
from .chessexception import ChessException
from .partialdisplay import DialoguePartialDisplay, DialoguePartialEdit


class ChessDBeditPartial(ChessException, DataEdit):
    """Dialog to edit a partial position on, or insert one into, database.

    The partial position is in it's own Toplevel widget.

    """

    def __init__(self, newobject, parent, oldobject, showinitial=True, ui=None):
        """Extend and create dialogue to edit or insert partial position."""
        if oldobject:
            title = ':  '.join((
                'Edit Partial Position',
                oldobject.value.get_name_text()))
        else:
            title = 'Insert Partial Position'
            showinitial = False
        self.__title = title.split(':')[0]
        if showinitial:
            showinitial = DialoguePartialDisplay(master=parent, ui=ui)
            if ui is not None:
                ui.partials_in_toplevels.add(showinitial)
            if oldobject.database is not None:
                showinitial.partial.extract_position(oldobject.get_srvalue())
            else:
                showinitial.partial.extract_position(
                    oldobject.get_srvalue_as_str())
            showinitial.partial.process_partial_position()
            showinitial.set_position()
        newview = DialoguePartialEdit(master=parent, ui=ui)
        if ui is not None:
            ui.partials_in_toplevels.add(newview)
        if newobject.database is not None:
            newview.partial.extract_position(newobject.get_srvalue())
        else:
            newview.partial.extract_position(newobject.get_srvalue_as_str())
        newview.partial.process_partial_position()
        newview.set_position()
        super(ChessDBeditPartial, self).__init__(
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
        self.newobject.value.load(repr(self.newview.get_name_position_text()))
        if not self.newobject.value.is_position():
            dialogues.showerror(
                title=self.__title,
                message=''.join(('No partial position given.\n\n',
                                 'Name of partial position must be first ',
                                 'line, and subsequent lines the position.',
                                 )))
            return False
        return super(ChessDBeditPartial, self).dialog_ok()

    def tidy_on_destroy(self):
        """Clear up after dialogue destruction."""
        self.ui.partials_in_toplevels.discard(self.oldview)
        self.ui.partials_in_toplevels.discard(self.newview)
        self.ui.base_partials.selection.clear()
