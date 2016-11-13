# selectionedit.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Edit a game selection rule and change main list of games to fit.

The SelectionEdit class displays a game selection rule and allows editing.

This class has the selection.Selection class as a superclass.

This class does not allow deletion of game selection rules from a database.

An instance of these classes fits into the user interface in two ways: as an
item in a panedwindow of the main widget, or as the only item in a new toplevel
widget.

"""

from ..core.selectionrule import SelectionRule
from .selection import Selection
from .eventspec import EventSpec


class SelectionEdit(Selection):
    
    """Display a game selection rule with editing allowed.
    """

    # True means selection selection can be edited
    _is_selection_editable = True

    def __init__(self, **ka):
        """Extend game selection rule widget as editor."""
        super(SelectionEdit, self).__init__(**ka)
        self.bind_pointer()
        # Context is same for each location so do not need dictionary of
        # SelectionRule instances.
        self.selection_token_checker = SelectionRule()

    def bind_for_viewmode(self):
        """Set keyboard bindings for game selection rule display."""
        super(SelectionEdit, self).bind_for_viewmode()
        for sequence, function in (
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    def bind_pointer(self):
        """Set pointer button-1 binding."""
        for sequence, function in (
            ('<Control-ButtonPress-1>', ''),
            ('<ButtonPress-1>', ''), # go_to_token
            ('<ButtonPress-3>', ''),
            ):
            self.score.bind(sequence, function)
        
    def set_selection_rule(self, **kargs):
        """Display the game selection rule as search creteria text."""
        super().set_selection_rule(**kargs)
        self.bind_for_viewmode()

    def disable_keyboard(self):
        """Override and do nothing."""
