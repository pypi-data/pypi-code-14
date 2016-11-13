# partial.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Display a partial position.

A partial position is a pattern of chess pieces used to select games which
contain position which match the pattern.

The Partial class displays a partial position.

An instance of these classes fits into the user interface in two ways: as an
item in a panedwindow of the main widget, or as the only item in a new toplevel
widget.

The partialedit module provides a subclass which allows editing in the main
application window.

The partialdbshow and partialdbedit modules provide subclasses used in a new
toplevel widget to display or edit partial positions.

The partialdbdelete module provides a subclass used in a new toplevel widget to
allow deletion of partial positions from a database.

"""
# Game (game.py) and Partial (partial.py) should be
# subclasses of some more basic class.  They are not because Game started
# as a game displayer while Partial started as a Text widget with no
# validation and they have been converging ever since.  Next step will get
# there.  Obviously this applies to subclasses GameEdit (gameedit.py)
# and PartialEdit (partialedit.py) as well.

import tkinter

from .board import PartialBoard
from .partialscore import PartialScore
from ..core import exporters
from .eventspec import EventSpec
    

class Partial(PartialScore):

    """Partial position widget composed from PartialBoard and Text widgets.
    """

    def __init__(
        self,
        master=None,
        boardfont=None,
        ui=None,
        items_manager=None,
        itemgrid=None,
        **ka):
        """Create widgets to display partial position.

        Create Frame in toplevel and add Canvas and Text.
        Text width and height set to zero so widget fit itself into whatever
        space Frame has available.
        Canvas must be square leaving Text at least half the Frame.

        """

        panel = tkinter.Frame(
            master,
            borderwidth=2,
            relief=tkinter.RIDGE)
        panel.bind('<Configure>', self.try_event(self.on_configure))
        panel.grid_propagate(False)
        board = PartialBoard(
            panel,
            boardfont=boardfont,
            ui=ui)
        super(Partial, self).__init__(
            panel,
            board,
            ui=ui,
            items_manager=items_manager,
            itemgrid=itemgrid,
            **ka)
        self.scrollbar.grid(column=2, row=0, rowspan=2, sticky=tkinter.NSEW)
        self.board.get_top_widget().grid(
            column=0, row=0, rowspan=1, sticky=tkinter.NSEW)
        self.score.grid(column=1, row=0, rowspan=2, sticky=tkinter.NSEW)
        if not ui.visible_scrollbars:
            panel.after_idle(self.hide_scrollbars)
        self.configure_partial_widget()

        # The popup menus specific to Partial (placed same as Game equivalent)

        self.viewmode_popup.add_cascade(
            label='Database', menu=self.viewmode_database_popup)
        for function, accelerator in (
            (self.export_partial, EventSpec.export_text_from_partial),
            ):
            self.viewmode_database_popup.add_command(
                label=accelerator[1],
                command=self.try_command(
                    function, self.viewmode_database_popup),
                accelerator=accelerator[2])

        # For compatibility with Game when testing if item has focus.
        self.takefocus_widget = self.score
        
    def bind_for_viewmode(self):
        """Set keyboard bindings for partial position display."""
        super(Partial, self).bind_for_viewmode()
        self._bind_export(True)
        
    def _bind_export(self, switch):
        """Set keyboard bindings for exporting games."""
        ste = self.try_event
        for sequence, function in (
            (EventSpec.export_text_from_partial,
             self.export_partial),
            ):
            self.score.bind(
                sequence[0],
                '' if not switch else '' if not function else ste(function))

    def destroy_widget(self):
        """Destroy the widget displaying partial position."""
        self.panel.destroy()

    def get_top_widget(self):
        """Return topmost widget for partial position display.

        The topmost widget is put in a container widget in some way
        """
        return self.panel

    def on_configure(self, event=None):
        """Reconfigure board and score after container has been resized."""
        self.configure_partial_widget()
        
    def configure_partial_widget(self):
        """Configure board and score widgets for a partial position display."""
        cw = self.panel.winfo_width()
        ch = self.panel.winfo_height()
        bd = self.panel.cget('borderwidth')
        a = ch - bd * 2
        b = cw - bd * 2
        x = (a + b) // 3
        if x * 3 > b * 2:
            x = (b * 2) // 3
        elif x > a:
            x = a
        self.panel.grid_rowconfigure(1, minsize=a - x)
        self.panel.grid_columnconfigure(1, minsize=b - x)
        self.panel.grid_rowconfigure(0, weight=1)
        self.panel.grid_rowconfigure(1, weight=0)
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.grid_columnconfigure(1, weight=1)
        self.panel.grid_columnconfigure(2, weight=0)

    def hide_scrollbars(self):
        """Hide the scrollbars in the partial position display widgets."""
        self.scrollbar.grid_remove()
        self.score.grid_configure(columnspan=2)
        self.configure_partial_widget()
        self.see_current_move()

    def show_scrollbars(self):
        """Show the scrollbars in the partial position display widgets."""
        self.score.grid_configure(columnspan=1)
        self.scrollbar.grid_configure()
        self.configure_partial_widget()
        self.see_current_move()

    def takefocus(self, take=True):
        """Configure game widget takefocus option."""

        # Hack because I misunderstood meaning of takefocus: FALSE does not
        # stop the widget taking focus, just stops tab traversal.
        if take:
            #self.takefocus_widget.configure(takefocus=tkinter.TRUE)
            self.takefocus_widget.configure(takefocus=tkinter.FALSE)
        else:
            self.takefocus_widget.configure(takefocus=tkinter.FALSE)

    def bind_board_pointer_for_board_navigation(self, switch):
        """Enable or disable bindings for game navigation."""
        self.bind_board_pointer_for_widget_navigation(False)

    def bind_board_pointer_for_widget_navigation(self, switch):
        """Enable or disable bindings for widget selection."""
        for sequence, function in (
            ('<Control-ButtonPress-1>', ''),
            ('<ButtonPress-1>', self.try_event(self.give_focus_to_widget)),
            ('<ButtonPress-3>', self.try_event(self.popup_inactive_menu)),
            ):
            for s in self.board.boardsquares.values():
                s.bind(sequence, '' if not switch else function)

    def bind_score_pointer_for_widget_navigation(self, switch):
        """Set or unset pointer bindings for widget navigation."""
        for sequence, function in (
            ('<Control-ButtonPress-1>', ''),
            ('<ButtonPress-1>', self.try_event(self.give_focus_to_widget)),
            ('<ButtonPress-3>', self.try_event(self.popup_inactive_menu)),
            ):
            self.score.bind(sequence, '' if not switch else function)

    def set_colours(self, sbg, bbg, bfg):
        """Set colours and fonts used to display games.

        sbg == True - set game score colours
        bbg == True - set board square colours
        bfg == True - set board piece colours

        """
        if sbg:
            self.score.tag_configure('l_color', background=self.l_color)
            self.score.tag_configure('m_color', background=self.m_color)
            self.score.tag_configure('am_color', background=self.am_color)
            self.score.tag_configure('v_color', background=self.v_color)
        if bbg:
            self.board.set_color_scheme()
        if bfg:
            self.board.draw_board()

    def export_partial(self, event=None):
        """Export displayed partial position definition."""
        exporters.export_single_position(
            self.score.get('1.0', tkinter.END),
            self.ui.get_export_filename_for_single_item(
                'Partial Position', pgn=False))
