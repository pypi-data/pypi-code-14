# partialedit.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Edit a partial position and put it on a board.

The PartialEdit class displays a partial position and allows editing.

This class has the partial.Partial class as a superclass.

This class does not allow deletion of partial positions from a database.

An instance of these classes fits into the user interface in two ways: as an
item in a panedwindow of the main widget, or as the only item in a new toplevel
widget.

"""

import tkinter

from basesup.tools.workarounds import text_count

from ..core.partialposition import PartialPosition
from .partial import Partial
from ..core.constants import (
    EDITCHARS,
    DESCRIPTIONCHARS,
    )
from .constants import (
    MOVE_TAG,
    NAVIGATE_TOKEN,
    INSERT_TOKEN_MARK,
    START_POSITION_MARK,
    START_EDIT_MARK,
    END_EDIT_MARK,
    PIECE_LOCATIONS,
    SPACE_SEP,
    TOKEN_MARK,
    TOKEN,
    ALTERNATIVE_MOVE_TAG,
    POSITION,
    DESCRIPTION,
    )
from .eventspec import EventSpec


class PartialEdit(Partial):
    
    """Display a partial position with editing allowed.
    """

    # True means partial position can be edited
    _is_partial_editable = True

    def __init__(self, **ka):
        """Extend partial position widget as editor."""
        super(PartialEdit, self).__init__(**ka)
        self.bind_pointer()
        for function, accelerator in (
            (self.show_prev_token,
             EventSpec.partialedit_show_previous_token),
            (self.show_next_token,
             EventSpec.partialedit_show_next_token),
            (self.show_first_token,
             EventSpec.partialedit_show_first_token),
            (self.show_last_token,
             EventSpec.partialedit_show_last_token),
            (self.insert_partial_name,
             EventSpec.partialedit_insert_partial_name_left),
            (self.insert_partial_name,
             EventSpec.partialedit_insert_partial_name_right),
            ):

            # Insert before database because the Game equivalents are set in
            # Score, a superclass of Game. which has no equivalent in Partial
            # chain.
            self.viewmode_popup.insert_command(
                'Database',
                label=accelerator[1],
                command=self.try_command(function, self.viewmode_popup),
                accelerator=accelerator[2])
            
        self._allowed_chars_in_token = EDITCHARS
        # Context is same for each location so do not need dictionary of
        # PartialPosition instances.
        self.partial_token_checker = PartialPosition()

    def insert_char_or_token(self, event):
        """"""
        # This method is more complex than it looks.
        # This method looks more complicated than you might think it should.
        # Some assumptions are made about the layout of tags in the Text
        # widget self.score and the behaviour may yet justify providing a
        # class per tag to make the methods simpler.  But this will involve
        # doing the same to the gameedit module.
        if not self.current:
            if self.score.compare(tkinter.INSERT, '>=', START_POSITION_MARK):
                if self.insert_piece_location(event.char):
                    return self.show_insert_token()
            elif event.char: # So Shift + char does what is wanted
                oldtoken = self.get_token_tag_of_index(tkinter.INSERT)
                self.map_position_description(event.char)
                self.score.delete(*self.score.tag_ranges(oldtoken))
                return self.show_insert_token()
        elif self.score.tag_nextrange(
            PIECE_LOCATIONS, *self.score.tag_ranges(self.current)):
            if self.insert_piece_location(event.char):
                return self.show_next_token()
        elif self.insert_char_to_right(event.char):
            self.process_location()
        return 'break'

    def bind_for_viewmode(self):
        """Set keyboard bindings for partial position display."""
        super(PartialEdit, self).bind_for_viewmode()
        for sequence, function in (
            (EventSpec.partialedit_insert_char_or_token,
             self.insert_char_or_token),
            (EventSpec.partialedit_delete_char_left,
             self.delete_char_left),
            (EventSpec.partialedit_delete_char_right,
             self.delete_char_right),
            (EventSpec.partialedit_show_previous_token,
             self.show_prev_token),
            (EventSpec.partialedit_show_next_token,
             self.show_next_token),
            (EventSpec.partialedit_show_first_token,
             self.show_first_token),
            (EventSpec.partialedit_show_last_token,
             self.show_last_token),
            (EventSpec.partialedit_insert_partial_name_left,
             self.insert_partial_name),
            (EventSpec.partialedit_insert_partial_name_right,
             self.insert_partial_name),
            (EventSpec.partialedit_set_insert_previous_char_in_token,
             self.set_insert_prev_char_in_token),
            (EventSpec.partialedit_set_insert_next_char_in_token,
             self.set_insert_next_char_in_token),
            (EventSpec.partialedit_set_insert_first_char_in_token,
             self.set_insert_first_char_in_token),
            (EventSpec.partialedit_set_insert_last_char_in_token,
             self.set_insert_last_char_in_token),
            ):
            if function:
                function = self.try_event(function)
            self.score.bind(sequence[0], function)

    def bind_pointer(self):
        """Set pointer button-1 binding.

        Always self.go_to_token in Score instances but subclasses should
        override as necessary.

        """
        for sequence, function in (
            ('<Control-ButtonPress-1>', ''),
            ('<ButtonPress-1>', self.try_event(self.go_to_token)),
            ('<ButtonPress-3>', ''),
            ):
            self.score.bind(sequence, function)

    def clear_current_range(self):
        """Remove existing MOVE_TAG ranges."""
        tr = self.score.tag_ranges(MOVE_TAG)
        if tr:
            self.score.tag_remove(MOVE_TAG, *tr)

    def delete_char_left(self, event):
        """"""
        if not self.current:
            return 'break'
        elif self.score.tag_nextrange(
            PIECE_LOCATIONS, *self.score.tag_ranges(self.current)):
            self.delete_char_next_to_insert_mark(
                START_EDIT_MARK, tkinter.INSERT)
        elif self.get_token_text_length(START_EDIT_MARK, END_EDIT_MARK) > 1:
            self.delete_char_next_to_insert_mark(
                START_EDIT_MARK, tkinter.INSERT)
        else:
            next_current = self.select_prev_token_in_partial()
            self.delete_token()
            self.current = next_current
            self.set_current()
        return 'break'

    def delete_char_next_to_insert_mark(self, first, last):
        """Delete char after INSERT mark if INSERT equals first, else before.

        (first, last) should be (START_EDIT_MARK, Tkinter.INSERT) or
        (Tkinter.INSERT, END_EDIT_MARK).  A character is deleted only if the
        count of characters between first and last is greater than zero.  One
        of the characters next to the INSERT mark is deleted depending on the
        equality of first and INSERT mark.  If leading characters exist for
        the token when the text length is zero, the last of these is tagged
        with MOVE_TEXT (instead of the token characters).

        """
        widget = self.score
        if self.get_token_text_length(first, last):
            self.process_location(addpiece=False)
            if widget.compare(first, '==', tkinter.INSERT):
                widget.delete(tkinter.INSERT)
            else:
                widget.delete(tkinter.INSERT + '-1 chars')
            if self.get_token_text_length(START_EDIT_MARK, END_EDIT_MARK) == 0:
                if self._lead: # self.current will have a range. Or test range.
                    widget.tag_add(
                        MOVE_TAG,
                        ''.join((
                            str(widget.tag_ranges(self.current)[0]),
                            ' +',
                            str(self._lead - 1),
                            'chars')))
            else:
                self.process_location(addpiece=True)
        
    def delete_char_right(self, event):
        """"""
        if not self.current:
            return 'break'
        elif self.score.tag_nextrange(
            PIECE_LOCATIONS, *self.score.tag_ranges(self.current)):
            self.delete_char_next_to_insert_mark(
                tkinter.INSERT, END_EDIT_MARK)
        elif self.get_token_text_length(START_EDIT_MARK, END_EDIT_MARK) > 1:
            self.delete_char_next_to_insert_mark(
                tkinter.INSERT, END_EDIT_MARK)
        else:
            next_current = self.select_prev_token_in_partial()
            self.delete_token()
            self.current = next_current
            self.set_current()
        return 'break'

    def delete_token(self):
        """"""
        if self.get_token_text_length(START_EDIT_MARK, END_EDIT_MARK) == 0:
            return
        tr = self.score.tag_ranges(
            self.get_token_tag_for_position(self.current))
        if tr:
            self.score.delete(*tr)
            # Only EDITCHARS allowed if partial position name absent or
            # deleted by current delete action.
            if self.score.compare(START_POSITION_MARK, '==', '1.0'):
                self._allowed_chars_in_token = EDITCHARS
            return

    def get_insertion_point_within_current(self):
        """"""
        if not self.current:
            return
        start, end = self.score.tag_ranges(self.current)
        mark = self.score.mark_next(start)
        while mark:
            if mark.startswith(TOKEN_MARK):
                if self.score.compare(mark, '>', end):
                    return
                else:
                    return mark
            else:
                mark = self.score.mark_next(mark)

    def get_insertion_point_at_end_of_current(self):
        """"""
        ip = self.score.tag_nextrange(
            NAVIGATE_TOKEN, self.score.tag_ranges(self.current)[-1])
        if ip:
            return ip[0]
        else:
            return self.score.index(tkinter.END)

    def get_position_tag_for_token(self, token):
        """Return Tk tag name for position with same suffix as token."""
        return ''.join((POSITION, position[len(TOKEN):]))

    def get_token_tag_for_position(self, position):
        """Return Tk tag name for token with same suffix as position."""
        return ''.join((TOKEN, position[len(POSITION):]))

    def get_token_text_length(self, start, end):
        """Return length of text between start and end indicies"""
        return text_count(self.score, start, end)

    def insert_partial_name(self, event=None):
        """Insert a tagged area for the partial position name."""
        tr = self.score.tag_ranges(DESCRIPTION)
        if self.score.compare(START_POSITION_MARK, '>', '1.0'):
            if tr:
                self.show_first_token()
            else:
                self.current = None
                self.set_marks_for_editing('1.0', '1.0')
            return
        elif tr:
            self.show_first_token()
        else:
            self.current = None
            self.map_position_description('')

    def insert_piece_location(self, char):
        """Insert first character of new piece location."""
        if not char:
            return
        if char not in EDITCHARS:
            return
        if self.current:
            self.score.mark_set(
                tkinter.INSERT,
                self.get_insertion_point_at_end_of_current())
        else:
            self.score.mark_set(tkinter.INSERT, START_POSITION_MARK)
        # The first character put in location token must give a location error
        # since piece locations have exactly three characters (Ke4 and so on).
        # There is no game context to worry about so just call the map_...
        # method, unlike the insert move into game score case.
        self.map_location_error_text(char)
        return True

    def map_location_error_text(self, token):
        """"""
        return self.tag_token_for_editing(
            super(PartialEdit, self).map_location_error_text(token),
            self.get_current_tag_and_mark_names,
            )

    def map_piecelocation_text(self, token):
        """"""
        return self.tag_token_for_editing(
            super(PartialEdit, self).map_piecelocation_text(token),
            self.get_current_tag_and_mark_names,
            )

    def map_position_description(self, token):
        """"""
        return self.tag_token_for_editing(
            super(PartialEdit, self).map_position_description(token),
            self.get_current_tag_and_mark_names,
            )

    def process_location(self, addpiece=True):
        """"""
        tr = self.score.tag_ranges(self.current)
        if self.score.tag_nextrange(DESCRIPTION, *tr):
            return
        token = self.score.get(*tr)
        self.partial_token_checker.extract_position(token)
        self.partial_token_checker.process_partial_position()
        if self.partial_token_checker.is_position():
            if addpiece:
                self.partial.set_board_piece(token)
                self.set_position_board()
                self.score.tag_remove(ALTERNATIVE_MOVE_TAG, *tr)
                self.score.tag_add(PIECE_LOCATIONS, *tr)
            else:
                token = list(token)
                token[0] = SPACE_SEP
                self.partial.set_board_piece(''.join(token))
                self.set_position_board()
                self.score.tag_remove(PIECE_LOCATIONS, *tr)
                self.score.tag_add(ALTERNATIVE_MOVE_TAG, *tr)

    def select_first_token_in_partial(self):
        """Return NAVIGATE_TOKEN range for first token in partial"""
        try:
            return self.get_position_tag_of_index(
                self.score.tag_nextrange(NAVIGATE_TOKEN, '1.0')[0])
        except IndexError:
            return None

    def select_insert_token_in_partial(self):
        """Return NAVIGATE_TOKEN range in partial containing INSERT mark"""
        try:
            return self.get_position_tag_of_index(
                self.score.tag_prevrange(NAVIGATE_TOKEN, tkinter.INSERT)[0])
        except IndexError:
            return None

    def select_last_token_in_partial(self):
        """Return NAVIGATE_TOKEN range for last token in partial"""
        try:
            return self.get_position_tag_of_index(
                self.score.tag_prevrange(NAVIGATE_TOKEN, tkinter.END)[0])
        except IndexError:
            return None

    def select_next_token_in_partial(self):
        """Return NAVIGATE_TOKEN range for next token in partial"""
        if not self.current:
            return self.select_first_token_in_partial()
        try:
            return self.get_position_tag_of_index(
                self.score.tag_nextrange(
                    NAVIGATE_TOKEN,
                    self.score.tag_ranges(self.current)[-1])[0])
        except IndexError:
            return None

    def select_prev_token_in_partial(self):
        """Return NAVIGATE_TOKEN range for previous token in partial"""
        if not self.current:
            return self.select_last_token_in_partial()
        try:
            return self.get_position_tag_of_index(
                self.score.tag_prevrange(
                    NAVIGATE_TOKEN,
                    self.score.tag_ranges(self.current)[0])[0])
        except IndexError:
            return None

    def set_insert_mark_at_end_of_token(self):
        """"""
        if self.current:
            self.score.mark_set(tkinter.INSERT, END_EDIT_MARK)
            self.set_insertion_point_within_current()
        
    def set_insert_mark_at_start_of_token(self):
        """"""
        if self.current:
            self.score.mark_set(tkinter.INSERT, START_EDIT_MARK)
            self.set_insertion_point_within_current()
        
    def set_insert_mark_left_one_char(self):
        """"""
        if self.current:
            if self.score.compare(tkinter.INSERT, '>', START_EDIT_MARK):
                self.score.mark_set(
                    tkinter.INSERT, tkinter.INSERT + ' -1 chars')
                self.set_insertion_point_within_current()
        
    def set_insert_mark_right_one_char(self):
        """"""
        if self.current:
            if self.score.compare(tkinter.INSERT, '<', END_EDIT_MARK):
                self.score.mark_set(
                    tkinter.INSERT, tkinter.INSERT + ' +1 chars')
                self.set_insertion_point_within_current()

    def set_insertion_point_within_current(self):
        """"""
        mark = self.get_insertion_point_within_current()
        if mark:
            self.score.mark_set(mark, tkinter.INSERT)
        
    def set_current(self):
        """Remove existing MOVE_TAG ranges and add self.current ranges.

        All characters have one tag which indicates the edit rules that apply
        to the token containing the character.  For non-location markers it is
        the absence of such a tag that indicates the rule.  Default is no
        editing.

        """
        self.set_current_range()
        if not self.current:
            self.score.mark_set(INSERT_TOKEN_MARK, START_POSITION_MARK)
            self.score.mark_set(tkinter.INSERT, INSERT_TOKEN_MARK)
            return
        self.score.mark_set(
            INSERT_TOKEN_MARK, self.score.tag_ranges(self.current)[1])
        self.score.mark_set(tkinter.INSERT, INSERT_TOKEN_MARK)
        self.set_marks_for_editing(*self.score.tag_ranges(self.current))

    def set_current_range(self):
        """Remove existing MOVE_TAG ranges and add self.currentmove ranges.

        Subclasses may adjust the MOVE_TAG range if the required colouring
        range of the item is different.  For example just <text> in {<text>}
        which is a PGN comment where <text> may be null after editing.

        The adjusted range must be a subset of self.currentmove range.

        """
        self.clear_current_range()

    def set_insert_first_char_in_token(self, event):
        """"""
        self.set_insert_mark_at_start_of_token()
        return 'break'

    def set_insert_last_char_in_token(self, event):
        """"""
        self.set_insert_mark_at_end_of_token()
        return 'break'

    def set_insert_next_char_in_token(self, event):
        """"""
        self.set_insert_mark_right_one_char()
        return 'break'

    def set_insert_prev_char_in_token(self, event):
        """"""
        self.set_insert_mark_left_one_char()
        return 'break'

    def set_marks_for_editing(self, start, end, lead_trail=(0, 0)):
        """Set token editing bound marks from start and end"""
        if self.score.compare(start, '<', START_POSITION_MARK):
            self._allowed_chars_in_token = DESCRIPTIONCHARS
        else:
            self._allowed_chars_in_token = EDITCHARS
        self._lead, self._trail = lead_trail
        self._header_length = self._lead + self._trail
        if self._lead:
            sem = self.score.index(
                ''.join((str(start), ' +', str(self._lead), ' chars')))
        else:
            sem = start
        if self._trail:
            eem = self.score.index(
                ''.join((str(end), ' -', str(self._trail), ' chars')))
        else:
            eem = end
        offset = self.get_token_text_length(start, end) - self._header_length
        if offset:
            if self._lead:
                start = sem
            if self._trail:
                end = eem
        else:
            if self._lead:
                start = self.score.index(''.join((str(sem), ' -1 chars')))
            end = sem
        mark = self.get_insertion_point_within_current()
        if mark:
            self.score.mark_set(tkinter.INSERT, mark)
        elif self.score.compare(tkinter.INSERT, '>', eem):
            self.score.mark_set(tkinter.INSERT, eem)
        elif self.score.compare(tkinter.INSERT, '<', sem):
            self.score.mark_set(tkinter.INSERT, sem)
        self.score.mark_set(START_EDIT_MARK, sem)
        self.score.mark_gravity(START_EDIT_MARK, 'left')
        self.score.mark_set(END_EDIT_MARK, eem)
        self.set_move_tag(start, end)

    def set_move_tag(self, start, end):
        """Add range start to end to MOVE_TAG (which is expected to be empty).

        Assumption is that set_current_range has been called and MOVE_TAG is
        still empty following that call.

        """
        self.score.tag_add(MOVE_TAG, start, end)

    def show_first_token(self, event=None):
        """Display first token in partial position (usually the name)."""
        self.current = self.select_first_token_in_partial()
        self.set_current()
        self.set_position_board()
        return 'break'
        
    def show_insert_token(self, event=None):
        """Display token containing INSERT mark."""
        self.current = self.select_insert_token_in_partial()
        self.set_current()
        self.set_position_board()
        return 'break'
        
    def show_last_token(self, event=None):
        """Display last token in partial position."""
        self.current = self.select_last_token_in_partial()
        self.set_current()
        self.set_position_board()
        return 'break'
        
    def show_next_token(self, event=None):
        """Display next token in partial position."""
        self.current = self.select_next_token_in_partial()
        self.set_current()
        self.set_position_board()
        return 'break'
        
    def show_prev_token(self, event=None):
        """Display previous token in partial position."""
        self.current = self.select_prev_token_in_partial()
        self.set_current()
        self.set_position_board()
        return 'break'
        
    def tag_token_for_editing(
        self,
        token_indicies,
        tag_and_mark_names,
        tag_start_to_end=(),
        tag_start_to_sepend=(),
        mark_for_edit=True,
        ):
        """Tag token for single-step navigation and game editing.

        token_indicies - the start end and separator end indicies of the token
        tag_and_mark_names - method which returns tag and mark names for token
        tag_start_to_end - state tags appropriate for editable text of token
        tag_start_to_sepend - state tags appropriate for token
        mark_for_edit - the insert index to be used when editing token

        tag_and_mark_names is a method name because in some cases the current
        names are needed and in others new names should be generated first:
        pass the appropriate method.

        """
        start, end, sepend = token_indicies
        tokenmark = tag_and_mark_names()[1]
        tag_add = self.score.tag_add
        for tag in tag_start_to_end:
            tag_add(tag, start, end)
        for tag in tag_start_to_sepend:
            tag_add(tag, start, sepend)
        if mark_for_edit:
            self.score.mark_set(tokenmark, end)
        return token_indicies

    def insert_char_to_right(self, char):
        """"""
        if not char:
            return
        if self._allowed_chars_in_token:
            if char not in self._allowed_chars_in_token:
                return
        widget = self.score
        start, end = self.score.tag_ranges(self.current)
        non_empty = self.get_token_text_length(start, end) - self._header_length
        # Cannot add to a piece position token with more than two characters
        if non_empty > 2:
            if self.score.compare(tkinter.INSERT, '>=', START_POSITION_MARK):
                return False
        insert = str(widget.index(tkinter.INSERT))
        copy_from_insert = widget.compare(start, '==', insert)
        # Inserting character so if a piece is at location remove it
        self.process_location(addpiece=False)
        widget.insert(tkinter.INSERT, char)
        if copy_from_insert:
            for tn in widget.tag_names(tkinter.INSERT):
                widget.tag_add(tn, insert)
        else:
            for tn in widget.tag_names(start):
                widget.tag_add(tn, insert)
        # MOVE_TAG must tag something if token has leading and trailing only.
        widget.tag_add(MOVE_TAG, insert)
        if not non_empty:
            widget.tag_remove(
                MOVE_TAG,
                ''.join((
                    str(start),
                    ' +',
                    str(self._lead - 1),
                    'chars')))
        return True

    def go_to_token(self, event=None):
        """Set position and highlighting for token under pointer"""
        if self.panel in self.itemmap:
            if self is not self.itemstack[-1].analysis:
                return 'break'
        self.go_to_piece(
            self.score.index(''.join(('@', str(event.x), ',', str(event.y)))))

    def go_to_piece(self, index):
        """Show position for piece text at index"""
        widget = self.score
        piece = widget.tag_nextrange(NAVIGATE_TOKEN, index)
        if not piece:
            piece = widget.tag_prevrange(NAVIGATE_TOKEN, index)
            if not piece:
                return
            elif widget.compare(piece[1], '<', index):
                return
        elif widget.compare(piece[0], '>', index):
            piece = widget.tag_prevrange(NAVIGATE_TOKEN, piece[0])
            if not piece:
                return
            if widget.compare(piece[1], '<', index):
                return
        selected_piece = self.get_position_tag_of_index(index)
        if selected_piece:
            self.current = selected_piece
            self.set_current()
            self.set_position_board()
            return True
        
    def set_position(self, **kargs):
        """Display the partial position as board and piece locations."""
        super().set_position(**kargs)
        self.bind_for_viewmode()

