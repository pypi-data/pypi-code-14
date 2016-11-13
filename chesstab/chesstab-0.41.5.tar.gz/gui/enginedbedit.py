# enginedbedit.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Customise edit dialogue to edit or insert chess engine definition record.
"""

from basesup.tools import dialogues

from .dataedit import DataEdit
from .chessexception import ChessException
from .enginedisplay import DialogueEngineDisplay, DialogueEngineEdit


class ChessDBeditEngine(ChessException, DataEdit):
    """Dialog to edit or insert a chess engine definition on database.

    The chess engine definition is in it's own Toplevel widget.

    """

    def __init__(self, newobject, parent, oldobject, showinitial=True, ui=None):
        """Create dialogue to edit or insert chess engine definition."""
        if oldobject:
            title = ':  '.join((
                'Edit Engine Definition',
                oldobject.value._description_string))
        else:
            title = 'Insert Engine Definition'
            showinitial = False
        self.__title = title.split(':')[0]
        if showinitial:
            showinitial = DialogueEngineDisplay(master=parent, ui=ui)
            if ui is not None:
                ui.engines_in_toplevels.add(showinitial)
            if oldobject.database is not None:
                showinitial.definition.extract_engine_definition(
                    oldobject.get_srvalue())
            else:
                showinitial.definition.extract_engine_definition(
                    oldobject.get_srvalue_as_str())
            #showinitial.definition.process_selection_rule()
            showinitial.set_engine_definition()
        newview = DialogueEngineEdit(master=parent, ui=ui)
        if ui is not None:
            ui.engines_in_toplevels.add(newview)
        if newobject.database is not None:
            newview.definition.extract_engine_definition(
                newobject.get_srvalue())
        else:
            newview.definition.extract_engine_definition(
                newobject.get_srvalue_as_str())
        #newview.definition.process_selection_rule()
        newview.set_engine_definition()
        super(ChessDBeditEngine, self).__init__(
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
        ed = self.newview.get_name_engine_definition_dict()
        if not ed:
            dialogues.showerror(
                title=self.__title,
                message=''.join(('No chess engine definition given.\n\n',
                                 'Name of chess engine definition must be ',
                                 'first line, and subsequent lines the ',
                                 'command to run the engine.',
                                 )))
            return False
        self.newobject.value.load(repr(ed))
        if not self.newobject.value.get_engine_command_text():
            dialogues.showerror(
                title=self.__title,
                message=''.join(('No chess engine definition given.\n\n',
                                 'Name of chess engine definition must be ',
                                 'first line, and subsequent lines the ',
                                 'command to run the engine.',
                                 )))
            return False
        return super(ChessDBeditEngine, self).dialog_ok()

    def tidy_on_destroy(self):
        """Clear up after dialogue destruction."""
        self.ui.engines_in_toplevels.discard(self.oldview)
        self.ui.engines_in_toplevels.discard(self.newview)

        # base_engines is None when this happens on Quit.
        try:
            self.ui.base_engines.selection.clear()
        except AttributeError:
            if self.ui.base_engines is not None:
                raise
