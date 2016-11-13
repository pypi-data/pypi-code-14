# partialposition.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Partial position parser.
"""

import re

from pgn.core.constants import (
    MAPFILE,
    MAPRANK,
    PIECES,
    NOPIECE,
    WPAWN,
    BPAWN,
    SCH,
    )

from .constants import (
    MAP_CH_TO_PARTIAL_PIECE,
    LOCATION,
    NAME_DELIMITER,
    SPLIT_INTO_TOKENS,
    POSITION_DESCRIPTION,
    )

_reglocation = re.compile(''.join((LOCATION, '\Z')))
re_tokens = re.compile(SPLIT_INTO_TOKENS)

_error = 1


class PartialPosition(object):
    """Partial position parser.

    Parse text for a partial position specification.
    
    """

    def __init__(self):
        """"""
        super(PartialPosition, self).__init__()
        self._state = None
        # The board is undefined.
        # piece_locations has slightly different meaning to similar attribute
        # in PGN from pgn.core.parser.
        # [0] is squares where piece on square is undefined
        # [1..12] is same
        # [13..16] are additional, meaning things like square is empty or
        # contains any white piece
        self.board_pieces = [NOPIECE] * 64
        self.position = []
        self.textok = ''
        self.texterror = ''
        #self.description = '' # partial position name displayed in record list
        # data generated from partial position text before validation
        self.tokens = []
        self._description_string = ''
        self._piecesquare_string = ''
        # data generated from partial position text after validation
        self.positiontokens = []
        # data structures to support display of partial positions
        # The performance overhead from putting this processing in the same
        # class as the parsing is insignificant, unlike the PGN case.
        self.locations = []

        self._despatch_table = {
            LOCATION: {
                None: self._process_location_or_whitespace,
                },
            None: {
                None: self._process_location_or_whitespace,
                },
            }
        
        self._unmatched_text_valid_table = {
            LOCATION: self._process_invalid_token,
            None: self._process_invalid_token,
            }

    def extract_position(self, text, delimiter=NAME_DELIMITER):
        """Return tuple(Name, Piece location text) for position in text."""
        # delimiter argument while database and display delimiters different
        position = [t.strip() for t in text.split(delimiter, 1)]
        if not len(position[0]) or not len(position[-1]):
            return False
        if len(position) == 1:
            self._description_string = ''
            self._piecesquare_string = position[0]
        else:
            self._description_string = position[0]
            self._piecesquare_string = position[1]
        return True

    def process_partial_position(self):
        """Extract partial position name and piece locations from position.

        position is a list or tuple of two strings.  First is position name
        and second is space separated piece locations.

        """
        self._partialtext_valid = True
        self._process_description()
        self.board_pieces = [NOPIECE] * 64
        self._state = LOCATION

        # Adjusted to fit 'FutureWarning: split() requires a non-empty pattern
        # match.' introduced at Python 3.5.
        self.tokens[:] = [t.strip()
                          for t in re_tokens.split(self._piecesquare_string)]

        self.positiontokens[:] = []
        self._process_partialtext()

    def get_name_text(self):
        """Return name text."""
        #convert unicode to str for Python26+
        return self._description_string

    def get_name_position_text(self):
        """Return name and position text."""
        #convert unicode to str for Python26+
        return NAME_DELIMITER.join(
            (self._description_string,
             self.get_position_text(delimiter=''),
             ))

    def get_position_text(self, delimiter=''):
        """Return position text."""
        return delimiter.join(self.positiontokens)

    def is_error(self):
        """Return True if parser is in error state."""
        return self._state == _error

    def is_position(self):
        """Return True if parser is in position found state."""
        return self._state == LOCATION

    def _process_description(self):
        self.locations[:] = [(POSITION_DESCRIPTION, self._description_string)]

    def _process_partialtext(self):
        # State table used for consistency with pgn processing but each token
        # is processed indenpendently at present.  It is possible that ( and )
        # will be added to be more selective in piece alternatives.
        dt = self._despatch_table
        utvt = self._unmatched_text_valid_table
        tokens = self.tokens
        for e, self._token in enumerate(tokens):
            if e % 2:
                dt[self._state].get(self._token, dt[self._state][None])()
            elif len(self._token):
                utvt[self._state]()
        self._set_partial_data()

    def _set_partial_data(self):
        """"""
        # Temporary while testing self._process_patialtext
        # textok and texterror will be replaced by inserting and tagging
        # the score widget in the display classes map_partial_position
        # method.  Similar to technique in game score processing.
        self.set_partial_position()
        self.textok = ' '.join(self.positiontokens)
        self.texterror = ''

    def _process_location_or_whitespace(self):
        if not len(self._token.strip()):
            return
        if self._token[0] in (WPAWN, BPAWN):
            if MAPRANK.get(self._token[-1]) in (0, 56):
                self.positiontokens.append(self._token)
                self._state = None
        self.set_board_piece(self._token)
        self.locations.append((LOCATION, len(self.positiontokens)))
        self.positiontokens.append(self._token)

    def _process_invalid_token(self):
        self.locations.append((None, len(self.positiontokens)))
        self.positiontokens.append(self._token)
        self._state = None

    def set_board_piece(self, t):
        piecename, file_, rank = t
        square = MAPFILE[file_] + MAPRANK[rank]
        if piecename in PIECES:
            self.board_pieces[square] = piecename
        else:
            piece = MAP_CH_TO_PARTIAL_PIECE.get(piecename, NOPIECE)
            self.board_pieces[square] = piece

    def set_partial_position(self):
        self.position = [p + SCH[s]
                         for s, p in enumerate(self.board_pieces)
                         if p != NOPIECE]

