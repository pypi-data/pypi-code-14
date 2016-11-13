# dbpartpos.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""bsddb interface to chess database for partial position index

There is no simple way of using bsddb cursors to do the index joins needed in
this module.  The Berkeley DB 'secondary database' method cannot be used
because the relevant substrings (Re1 and so on) of the values in game records
are instructions for generating secondary keys; not data that can be used as
secondary keys.  And the bsddb interface is now about following the DPT
interface to ease application problem fixing rather than being as quick as
possible itself.

List of classes

PartialPositionDS - represent subset of games that match a partial postion

"""

from gridsup.db.dbdatasource import DBDataSource

from pgn.core.constants import (
    PIECES,
    )

from ..core.constants import (
    MAP_PARTIAL_PIECE_TO_CH,
    MAP_PARTIAL_PIECE_TO_PIECES,
    NULLPIECE,
    ANY_WHITE_PIECE,
    ANY_BLACK_PIECE,
    PIECE_SQUARE_NOT_ALLOWED,
    )

from ..core.filespec import PIECESQUAREMOVE_FIELD_DEF, RESULT_FIELD_DEF


class PartialPositionDS(DBDataSource):
    
    """Extend to represent subset of games on file that match partial postion.

    Methods added:

    get_partial_position_games - Select games which match partial position

    Methods overridden:

    None
    
    Methods extended:

    __init__
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        super(PartialPositionDS, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

    def get_partial_position_games(self, partialposition, sourceobject):
        """Find game records matching partial position.

        A Python list and a custom cursor are used to simulate DPT foundset

        """
        if not partialposition:
            self.set_recordset([])
            return

        # Expand the partial position specification, which may include wildcard
        # pieces, to refer to the squares and pieces involved.
        # NOPIECE means the square is not used when evaluating the search.
        # A wildcard piece, NULLPIECE, is used to specify an empty square.
        position = []
        occupied_square_count = 0
        for sp in partialposition:
            partialpiece, square = sp
            if partialpiece in MAP_PARTIAL_PIECE_TO_PIECES:
                position.append((ord(square), partialpiece))
                if partialpiece != NULLPIECE:
                    occupied_square_count += 1
            elif partialpiece in PIECES:
                position.append((ord(square), partialpiece))
                occupied_square_count += 1
        if not position:
            self.set_recordset([])
            return

        # Ok to use CursorDB._cursor methods because result uses database
        # engine specific methods.  In Berkley DB must simulate an index
        # file with a Python list while DPT uses its list type.
        cursordb = self.dbhome.database_cursor(
            self.dbset, PIECESQUAREMOVE_FIELD_DEF)
        cursor = cursordb._cursor

        # Start with a square occupied by a particular piece if possible.
        # Otherwise prefer a square that specifies occupation by pieces of one
        # side as that means searching on six pieces rather than twelve.
        for i in range(len(position)):
            piecesquarebase = position.pop()
            square, partialpiece = piecesquarebase
            if partialpiece in PIECES:
                break
            position.insert(0, piecesquarebase)
        else:
            for i in range(len(position)):
                piecesquarebase = position.pop()
                square, partialpiece = piecesquarebase
                if partialpiece in (ANY_WHITE_PIECE, ANY_BLACK_PIECE):
                    break
                position.insert(0, piecesquarebase)
            else:
                piecesquarebase = position.pop()
                square, partialpiece = piecesquarebase

        pieces = MAP_PARTIAL_PIECE_TO_PIECES.get(partialpiece, (partialpiece,))

        movepiecesquare = dict()
        for p in pieces:
            if (p, square) in PIECE_SQUARE_NOT_ALLOWED:
                continue
            psb = self.dbhome.encode_record_selector(p + chr(square))
            pslen = len(psb)
            r = cursor.set_range(psb)
            while r is not None:
                piecesquaremove, game = r
                if not piecesquaremove.startswith(psb):
                    break
                movepiecesquare.setdefault(
                    piecesquaremove[pslen:], dict()).setdefault(
                        piecesquarebase, set()).add(game)
                r = cursor.next()
        
        for piecesquare in position:
            square, partialpiece = piecesquare
            pieces = MAP_PARTIAL_PIECE_TO_PIECES.get(
                partialpiece, (partialpiece,))
            for p in pieces:
                if (p, square) in PIECE_SQUARE_NOT_ALLOWED:
                    continue
                psb = self.dbhome.encode_record_selector(p + chr(square))
                pslen = len(psb)
                r = cursor.set_range(psb)
                while r is not None:
                    piecesquaremove, game = r
                    if not piecesquaremove.startswith(psb):
                        break
                    move = piecesquaremove[pslen:]
                    if move in movepiecesquare:
                        movepiecesquare[move].setdefault(
                            piecesquare, set()).add(game)
                    r = cursor.next()

        del cursor
        cursordb.close()

        # Provided there is at least one square with a piece other than
        # NULLPIECE specified there is at least one set of lists of games, one
        # for each move, which can be treated as the lists of all games on the
        # database for the evaluation of the search.
        cursordb = self.dbhome.database_cursor(self.dbset, RESULT_FIELD_DEF)
        cursor = cursordb._cursor

        allgames = set()
        r = cursor.first()
        while r is not None:
            allgames.add(r[1])
            r = cursor.next()

        del cursor
        cursordb.close()

        games = set()
        movegames = set()
        for move, moveposition in movepiecesquare.items():
            if len([p for sq, p in moveposition
                    if p != NULLPIECE]) < occupied_square_count:
                # At least one <piece, square> contributes no games for move
                # (allowing for position.pop() earlier).
                # The algorithm below will find games that meet at least one of
                # the <piece, square> conditions if allowed to proceed.
                # If 'a1' through 'h2' are specified as empty, '-b1' and so on,
                # with no other conditions all games are found; while if these
                # squares are specified as containing white pieces, 'Xg1' and
                # so on, no games are probably found even though it is initial
                # position of game.  The initial position is not indexed.
                continue
            movegames |= allgames
            for squarepiece, piecesquaremovegames in moveposition.items():
                if squarepiece[1] != NULLPIECE: 
                    # Square must be occupied.
                    # AND the games found for one piece square specification on
                    # a particular move with the games found for previously
                    # processed piece square specifications for that move.
                    movegames &= piecesquaremovegames
                else:
                    # Square must be unoccupied.
                    # Remove the games found for one piece square specification
                    # on a particular move from the games found for previously
                    # processed piece square specifications for that move and
                    # prevent other specifications restoring these games to the
                    # list for this move.
                    movegames &= allgames - piecesquaremovegames
            # OR the games found for the position specification on a particular
            # move with the games found on previously processed moves for the
            # position specification
            games |= movegames
            # Do not bother to clear movegames as it is filled with allrecords
            # before next use.

        # Build the list of game records
        cursordb = self.dbhome.database_cursor(self.dbset, self.dbname)
        cursor = cursordb._cursor
        recordset = []
        for g in sorted(games):
            r = cursor.set(self.dbhome.decode_record_number(g))
            if r:
                recordset.append(r)
        del cursor
        cursordb.close()

        # Hand the list of games over to the user interface.
        self.set_recordset(recordset)

