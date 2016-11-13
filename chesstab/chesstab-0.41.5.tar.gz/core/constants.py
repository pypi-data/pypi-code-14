# constants.py
# Copyright 2010 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Constants for partial position parser.

Uses pgn.core.constants values plus additional piece encodings for any piece,
any white piece, and so on.

"""

from pgn.core.constants import (
    MAPFILE,
    MAPRANK,
    NOPIECE,
    WKING,
    WQUEEN,
    WROOK,
    WBISHOP,
    WKNIGHT,
    WPAWN,
    BKING,
    BQUEEN,
    BROOK,
    BBISHOP,
    BKNIGHT,
    BPAWN,
    SCH,
    BOARDSIDE,
    BOARDSQUARES,
    )

ANY_PIECE = '?'
ANY_WHITE_PIECE = 'X'
ANY_BLACK_PIECE = 'x'
NULLPIECE = '-' # NOPIECE means any or no piece in partial positions
ANY_PIECE_CH = '?'
ANY_WHITE_PIECE_CH = 'X'
ANY_BLACK_PIECE_CH = 'x'
NULLPIECE_CH = '-'
MAP_CH_TO_PARTIAL_PIECE = {
    ANY_PIECE_CH: ANY_PIECE,
    ANY_WHITE_PIECE_CH: ANY_WHITE_PIECE,
    ANY_BLACK_PIECE_CH: ANY_BLACK_PIECE,
    NULLPIECE_CH: NULLPIECE,
    }
MAP_PARTIAL_PIECE_TO_CH = {
    ANY_PIECE: ANY_PIECE_CH,
    ANY_WHITE_PIECE: ANY_WHITE_PIECE_CH,
    ANY_BLACK_PIECE: ANY_BLACK_PIECE_CH,
    NULLPIECE: NULLPIECE_CH,
    }
MAP_PARTIAL_PIECE_TO_PIECES = {
    ANY_PIECE: (WKING, WQUEEN, WROOK, WBISHOP, WKNIGHT, WPAWN,
                BKING, BQUEEN, BROOK, BBISHOP, BKNIGHT, BPAWN,),
    ANY_WHITE_PIECE: (WKING, WQUEEN, WROOK, WBISHOP, WKNIGHT, WPAWN,),
    ANY_BLACK_PIECE: (BKING, BQUEEN, BROOK, BBISHOP, BKNIGHT, BPAWN,),
    NULLPIECE: (WKING, WQUEEN, WROOK, WBISHOP, WKNIGHT, WPAWN,
                BKING, BQUEEN, BROOK, BBISHOP, BKNIGHT, BPAWN,),
    }
POSITION_DESCRIPTION = 'description'
NAME_DELIMITER = '@'
LOCATION = ''.join((
    '[',
    NULLPIECE_CH, ANY_PIECE_CH, ANY_WHITE_PIECE_CH, ANY_BLACK_PIECE_CH,
    'kbnqrpKBNQRP][a-h][1-8]'))

# Adjusted to fit 'FutureWarning: split() requires a non-empty pattern match.'
# introduced at Python 3.5.
SPLIT_INTO_TOKENS = ''.join((
    '(',
    ''.join((LOCATION, '\s*')),
    ')',
    ))

EDITCHARS = ''.join(sorted(''.join((
    ANY_PIECE_CH, ANY_WHITE_PIECE_CH, ANY_BLACK_PIECE_CH, NULLPIECE_CH,
    'kbnqrpKBNQRPacdefgh12345678'))))
DESCRIPTIONCHARS = ''.join(sorted(''.join(
    (' ()1234567890',
     'abcdefghijklmnopqrstuvwxyz',
     'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
     ))))

PIECE_SQUARE_NOT_ALLOWED = set()
for _piece in WPAWN, BPAWN:
    for _square in range(BOARDSIDE):
        PIECE_SQUARE_NOT_ALLOWED.add((_piece, _square))
        PIECE_SQUARE_NOT_ALLOWED.add((_piece, BOARDSQUARES - _square - 1))
PIECE_SQUARE_NOT_ALLOWED = frozenset(PIECE_SQUARE_NOT_ALLOWED)

del _piece, _square, BOARDSIDE, BOARDSQUARES
