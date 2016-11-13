# partialscore.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Display the text defining a partial position.

The partial position is put on the instance's board.PartialBoard widget.

"""
# Not sure what to call this yet.
# See the similar comment at top of score.py.

# The following note is copied from the top of the game module.  PartialScore
# is not the 'more basic class' implied in the note.

# Game (game.py) and Partial (partial.py) should be
# subclasses of some more basic class.  They are not because Game started
# as a game displayer while Partial started as a Text widget with no
# validation and they have been converging ever since.  Next step will get
# there.  Obviously this applies to subclasses GameEdit (gameedit.py)
# and PartialEdit (partialedit.py) as well.

import tkinter

from .chessexception import ChessException
from .constants import (
    MOVE_COLOR,
    ALTERNATIVE_MOVE_COLOR,
    MOVE_TAG,
    ALTERNATIVE_MOVE_TAG,
    START_POSITION_MARK,
    DESCRIPTION,
    PIECE_LOCATIONS,
    NAVIGATE_TOKEN,
    SPACE_SEP,
    NEWLINE_SEP,
    TOKEN_MARK,
    TOKEN,
    POSITION,
    )
from ..core.partialposition import PartialPosition
from ..core.constants import (
    EDITCHARS,
    LOCATION,
    POSITION_DESCRIPTION,
    NAME_DELIMITER,
    )
from .eventspec import EventSpec
from .displayitems import DisplayItemsStub
    

class PartialScore(ChessException):

    """Chess partial position widget built from Text and Scrollbar widgets.
    """

    m_color = MOVE_COLOR
    am_color = ALTERNATIVE_MOVE_COLOR

    # True means partial position can be edited
    _is_partial_editable = False

    def __init__(
        self,
        panel,
        board,
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
        super(PartialScore, self).__init__(**ka)
        self.ui = ui

        # May be worth using a Null() instance for these two attributes.
        if items_manager is None:
            items_manager = DisplayItemsStub()
        self.items = items_manager
        self.itemgrid = itemgrid

        self.panel = panel
        self.board = board
        self.score = tkinter.Text(
            master=self.panel,
            width=0,
            height=0,
            takefocus=tkinter.FALSE,
            undo=True,
            wrap=tkinter.WORD)
        self.score.tag_configure(ALTERNATIVE_MOVE_TAG, background=self.am_color)
        self.score.tag_configure(MOVE_TAG, background=self.m_color)
        self.scrollbar = tkinter.Scrollbar(
            master=self.panel,
            orient=tkinter.VERTICAL,
            takefocus=tkinter.FALSE,
            command=self.score.yview)
        self.score.configure(yscrollcommand=self.scrollbar.set)

        # Keyboard actions do nothing by default.
        self.score.bind(EventSpec.partialscore_disable_keypress[0],
                        lambda e: 'break')

        # The popup menus for the partial position

        self.viewmode_popup = tkinter.Menu(master=self.score, tearoff=False)
        self.viewmode_database_popup = tkinter.Menu(
            master=self.viewmode_popup, tearoff=False)
        self.inactive_popup = None
        self.viewmode_navigation_popup = None

        self.current = None

        # Partial position parser instance to process text.
        self.partial = PartialPosition()
        self.location_number = 0

    def add_navigation_to_viewmode_popup(self, **kwargs):
        '''Add 'Navigation' entry to popup if not already present.'''

        # Cannot see a way of asking 'Does entry exist?' other than:
        try:
            self.viewmode_popup.index('Navigation')
        except:
            self.viewmode_navigation_popup = tkinter.Menu(
                master=self.viewmode_popup, tearoff=False)
            self.viewmode_popup.add_cascade(
                label='Navigation', menu=self.viewmode_navigation_popup)
            self.bind_navigation_for_viewmode_popup(**kwargs)
        
    def bind_for_viewmode(self):
        """Set keyboard bindings for partial position display."""

    def bind_navigation_for_viewmode_popup(self, bindings=None, order=None):
        """Set popup bindings for toplevel navigation."""
        if order is None:
            order = ()
        if bindings is None:
            bindings = {}
        for label, accelerator in order:
            function = bindings.get(label)
            if function is not None:
                self.viewmode_navigation_popup.add_command(
                    label=label,
                    command=self.try_command(
                        function, self.viewmode_navigation_popup),
                    accelerator=accelerator)

    def bind_score_pointer_for_board_navigation(self, switch):
        """Set or unset pointer bindings for partial position navigation."""
        ste = self.try_event
        for sequence, function in (
            ('<Control-ButtonPress-1>', ''),
            ('<ButtonPress-1>', ''),
            ('<ButtonPress-3>', ste(self.popup_viewmode_menu)),
            ):
            self.score.bind(sequence, '' if not switch else function)

    def get_current_tag_and_mark_names(self):
        """Return suffixed POSITION and TOKEN tag and TOKEN_MARK mark names."""
        suffix = str(self.location_number)
        return [''.join((t, suffix)) for t in (POSITION, TOKEN, TOKEN_MARK)]

    def give_focus_to_widget(self, event=None):
        """Do nothing and return 'break'.  Override in subclasses as needed."""
        return 'break'
        
    def see_first_piece(self):
        """Make first piece visible.

        Current piece is always made visible but no current piece defined
        for initial display.
        
        """
        self.score.see(START_POSITION_MARK)
        
    def see_current_move(self):
        """Make current piece visible and default to first piece"""
        if self.current:
            self.score.see(self.score.tag_ranges(self.current)[0])
        else:
            self.see_first_piece()
        
    def set_position_board(self):
        """Display partial position on board."""
        self.board.set_board(self.partial.board_pieces)
        
    def set_position(self, reset_undo=False):
        """Display the partial position as board and piece locations.
        
        reset_undo causes the undo redo stack to be cleared if True.  Set True
        on first display of a partial position for editing so that repeated
        Ctrl-Z in text editing mode recovers the original partial position.
        
        """
        if not self._is_partial_editable:
            self.score.configure(state=tkinter.NORMAL)
        self.score.delete('1.0', tkinter.END)
        self.map_partialposition()
        if not self._is_partial_editable:
            self.score.configure(state=tkinter.DISABLED)
        if reset_undo:
            self.score.edit_reset()
        self.board.set_board(self.partial.board_pieces)
        
    def set_statusbar_text(self):
        """Set status bar to display partial position name."""
        self.ui.statusbar.set_status_text(self.partial.get_name_text())

    def get_name_position_text(self):
        """"""
        text = []
        start = '1.0'
        while True:
            tr = self.score.tag_nextrange(NAVIGATE_TOKEN, start)
            if tr:
                text.append(self.score.get(*tr))
                start = tr[-1]
            else:
                break
        if not text:
            return NAME_DELIMITER
        if self.score.tag_ranges(DESCRIPTION):
            name = text.pop(0)
        else:
            name = ''
        return NAME_DELIMITER.join((name, ''.join(text)))

    def get_next_tag_and_mark_names(self):
        """Return next tag and mark names."""
        self.location_number += 1
        return self.get_current_tag_and_mark_names()

    def get_position_tag_of_index(self, index):
        """Return Tk tag name if index is in a position tag"""
        for tn in self.score.tag_names(index):
            if tn.startswith(POSITION):
                return tn
        return None

    def get_token_tag_of_index(self, index):
        """Return Tk tag name if index is in TOKEN tag"""
        for tn in self.score.tag_names(index):
            if tn.startswith(TOKEN):
                return tn
        return None

    def insert_token_into_text(self, token, separator):
        """Insert token and separator in widget.  Return boundary indicies.

        Indicies for start and end of token text are noted primarily to control
        editing and highlight significant text.  The end of separator index is
        used to generate contiguous regions for related tokens and act as a
        placeholder when there is no text between start and end.

        """
        widget = self.score
        start = widget.index(tkinter.INSERT)
        widget.insert(tkinter.INSERT, token)
        end = widget.index(tkinter.INSERT)
        widget.insert(tkinter.INSERT, separator)
        return start, end, widget.index(tkinter.INSERT)

    def map_partialposition(self):
        """."""
        dispatch_table = {
            LOCATION: self.map_piecelocation_text,
            None: self.map_location_error_text,
            }

        # Put the START_POSITION_MARK at the start of self.score by default.
        # self.map_position_description will move it to just after the newline
        # separator at the end of the partial position name.
        self.score.mark_set(START_POSITION_MARK, '1.0')

        positiontokens = self.partial.positiontokens
        for location in self.partial.locations:
            type_, token_descriptor = location
            try:
                dispatch_table[type_](positiontokens[token_descriptor])
            except KeyError:
                if type_ is POSITION_DESCRIPTION:
                    self.map_position_description(token_descriptor)

        # If there are no tokens move START_POSITION_MARK to the start of the
        # second line if it exists.
        tr = self.score.tag_prevrange(NAVIGATE_TOKEN, tkinter.END)
        if not tr:
            self.score.mark_set(START_POSITION_MARK, '1.0 +1 line')
        self.score.mark_gravity(START_POSITION_MARK, tkinter.LEFT)
        self.score.mark_set(tkinter.INSERT, START_POSITION_MARK)

    def map_location_error_text(self, token):
        """"""
        widget = self.score
        locationtag, tokentag, tokenmark = self.get_next_tag_and_mark_names()
        start, end, sepend = self.insert_token_into_text(token, SPACE_SEP)
        for tag in locationtag, NAVIGATE_TOKEN, ALTERNATIVE_MOVE_TAG:
            widget.tag_add(tag, start, end)
        widget.tag_add(tokentag, start, sepend)
        return start, end, sepend

    def map_piecelocation_text(self, token):
        """"""
        widget = self.score
        locationtag, tokentag, tokenmark = self.get_next_tag_and_mark_names()
        start, end, sepend = self.insert_token_into_text(token, SPACE_SEP)
        for tag in locationtag, PIECE_LOCATIONS, NAVIGATE_TOKEN:
            widget.tag_add(tag, start, end)
        widget.tag_add(tokentag, start, sepend)
        return start, end, sepend

    def map_position_description(self, token):
        """"""
        widget = self.score
        locationtag, tokentag, tokenmark = self.get_next_tag_and_mark_names()
        start, end, sepend = self.insert_token_into_text(token, NEWLINE_SEP)
        for tag in locationtag, DESCRIPTION, NAVIGATE_TOKEN:
            widget.tag_add(tag, start, end)
        widget.tag_add(tokentag, start, sepend)
        self.score.mark_set(START_POSITION_MARK, sepend)
        return start, end, sepend
        
    def popup_inactive_menu(self, event=None):
        """Show the popup menu for a score in an inactive item.

        Subclasses may have particular entries to be the default which is
        implemented by overriding this method.

        """
        self.inactive_popup.tk_popup(*self.score.winfo_pointerxy())
        
    def popup_viewmode_menu(self, event=None):
        """Show the popup menu for partial position actions.

        Subclasses define particular entries for this menu.  This class adds
        no items to the menu.

        """
        self.viewmode_popup.tk_popup(*self.score.winfo_pointerxy())
        
    def get_partial_key_partial_position(self):
        """Return partial position for use as partial key."""
        if self.partial.is_position():

            # Things must be arranged so a tuple, not a list, can be returned.
            return tuple(self.partial.position)
        
        else:
            return False

    def set_game_list(self):
        """Display games with position matching selected partial position.

        Deciding what to display in positionlist is not as neat as could be.

        Especially use of p.partial which is an object containing data from
        which keys are derived rather than the key itself.

        """
        grid = self.itemgrid
        if grid is None:
            return
        if grid.get_database() is not None:
            newpartialkey = self.get_partial_key_partial_position()
            if grid.partial != newpartialkey:
                grid.partial = newpartialkey
                grid.rows = 1
                grid.close_client_cursor()
                grid.datasource.get_partial_position_games(
                    newpartialkey,
                    self.recalculate_after_edit)
                grid.load_new_index()

                # Get rid of the 'Please wait ...' status text.
                self.ui.statusbar.set_status_text()
