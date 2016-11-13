# sqlite3partposbit.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""sqlite3 interface to chess database for partial position index

No attempt has been made to use the select statement to do the 'joins'.  The
algorithm used in the dpt and db modules has been adapted.

List of classes

PartialPositionDS - represent subset of games that match a partial postion

"""

from gridsup.apsw.sqlite3bitdatasource import Sqlite3bitDataSource

from basesup.api.recordset import Recordset
from basesup.api.constants import (
    SQLITE_SEGMENT_COLUMN,
    SQLITE_COUNT_COLUMN,
    )

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

from ..core.filespec import (
    PIECESQUAREMOVE_FIELD_DEF,
    PARTIAL_FILE_DEF,
    NEWGAMES_FIELD_DEF,
    _NEWGAMES_FIELD_VALUE,
    PARTIALPOSITION_FIELD_DEF,
    )


class PartialPositionDS(Sqlite3bitDataSource):
    
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
        games = Recordset(self.dbhome, self.dbset)
        if not partialposition:
            self.set_recordset(games)
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
            self.set_recordset(games)
            return

        # Use the previously calculated record set if possible
        if sourceobject is not None:
            ppview = self.dbhome.make_recordset_key(
                PARTIAL_FILE_DEF,
                PARTIAL_FILE_DEF,
                key=sourceobject.key.recno)
            changed = self.dbhome.make_recordset_key(
                PARTIAL_FILE_DEF,
                NEWGAMES_FIELD_DEF,
                key=self.dbhome.encode_record_selector(_NEWGAMES_FIELD_VALUE))
            pprecalc = ppview & changed
            changed.close()
            if pprecalc.count_records() == 0:
                ppcalc = self.dbhome.make_recordset_key_startswith(
                    self.dbset,
                    PARTIALPOSITION_FIELD_DEF,
                    key=self.dbhome.encode_record_number(
                        sourceobject.key.recno))
                if ppcalc.count_records() != 0:
                    calc = self.dbhome.make_recordset_key(
                        self.dbset,
                        PARTIALPOSITION_FIELD_DEF,
                        key=self.dbhome.encode_record_number(
                            sourceobject.key.recno))
                    games |= calc
                    self.set_recordset(games)
                    calc.close()
                    ppcalc.close()
                    ppview.close()
                    pprecalc.close()
                    return
                ppcalc.close()
            pprecalc.close()
        
        # Ok to use CursorSqlite3._cursor methods because result uses database
        # engine specific methods.  In Berkley DB must simulate an index
        # file with a Python list while DPT uses its list type.
        gamedb = self.dbhome.get_database_instance(
            self.dbset, PIECESQUAREMOVE_FIELD_DEF)
        if gamedb is None:
            return

        # Search the PieceSquareMove index for keys that match the position
        # specification and arrange them for the convenience of subsequent
        # FIND RECORDS operations to generate the list of games.
        # It is assumed that the presence of a key value in the index implies
        # the existence of at least one record (a game) where the piece is on
        # the square at the move.
        movepiecesquare = dict()
        piecesquarebase = position.pop()
        square, partialpiece = piecesquarebase
        pieces = MAP_PARTIAL_PIECE_TO_PIECES.get(partialpiece, (partialpiece,))
        for p in pieces:
            if (p, square) in PIECE_SQUARE_NOT_ALLOWED:
                continue
            psb = p + chr(square)
            pslen = len(psb)
            statement = ' '.join((
                'select',
                gamedb._fd_name, ',',
                SQLITE_SEGMENT_COLUMN, ',',
                SQLITE_COUNT_COLUMN, ',',
                gamedb._primaryname,
                'from',
                gamedb._fd_name,
                'where',
                gamedb._fd_name, 'glob ?',
                ))
            values = (self.dbhome.encode_record_selector(''.join((psb, '*'))),)
            for record in gamedb.sq_conn.cursor(
                ).execute(statement, values):
                movepiecesquare.setdefault(
                    record[0][pslen:], dict()).setdefault(
                        piecesquarebase, {})[record[1]] = record[2:]

        for piecesquare in position:
            square, partialpiece = piecesquare
            pieces = MAP_PARTIAL_PIECE_TO_PIECES.get(
                partialpiece, (partialpiece,))
            for p in pieces:
                if (p, square) in PIECE_SQUARE_NOT_ALLOWED:
                    continue
                psb = p + chr(square)
                pslen = len(psb)
                statement = ' '.join((
                    'select',
                    gamedb._fd_name, ',',
                    SQLITE_SEGMENT_COLUMN, ',',
                    SQLITE_COUNT_COLUMN, ',',
                    gamedb._primaryname,
                    'from',
                    gamedb._fd_name,
                    'where',
                    gamedb._fd_name, 'glob ?',
                    ))
                values = (
                    self.dbhome.encode_record_selector(''.join((psb, '*'))),)
                for record in gamedb.sq_conn.cursor().execute(
                    statement, values):
                    move = record[0][pslen:]
                    if move in movepiecesquare:
                        movepiecesquare[move].setdefault(
                            piecesquare, {})[record[1]] = record[2:]

        # Find the games using the position specification in movepiecesquare.
        allgames = self.dbhome.make_recordset_all(self.dbset, self.dbname)
        movegames = Recordset(self.dbhome, self.dbset)
        piecesquaregames = Recordset(self.dbhome, self.dbset)
        piecesquaremovegames = Recordset(self.dbhome, self.dbset)
        invertedpiecesquaremovegames = Recordset(self.dbhome, self.dbset)
        segmentgames = Recordset(self.dbhome, self.dbset)
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
            segments = None
            for s in [p.keys() for p in moveposition.values()]:
                if segments is None:
                    segments = set(s)
                else:
                    segments.intersection_update(s)
                if not len(segments):
                    break
            if not segments:
                # The <piece, square>s have no file segments in common.
                # Therefore there are no matching records on this move.
                continue
            movegames |= allgames
            for specpiece, psm in moveposition.items():
                for segment, reference in psm.items():
                    # OR the games found for each piece specified for a square
                    # on a particular move with the games found for previously
                    # processed pieces for that square and move.
                    piecesquaremovegames |= self.dbhome.recordset_for_segment(
                        segmentgames, PIECESQUAREMOVE_FIELD_DEF,
                        (self.dbset, segment, reference[0], reference[1]))
                if specpiece[1] == NULLPIECE:
                    # The square must be empty.
                    # piecesquaremovegames is the games where the square has
                    # a piece so invert the list.
                    invertedpiecesquaremovegames |= allgames
                    invertedpiecesquaremovegames |= piecesquaremovegames
                    invertedpiecesquaremovegames ^= piecesquaremovegames
                    piecesquaremovegames.clear_recordset()
                    piecesquaremovegames |= invertedpiecesquaremovegames
                    # Do not bother to clear invertedpiecesquaremovegames as it
                    # is filled with allrecords before next use.
                # AND the games found for one piece square specification on
                # a particular move with the games found for previously
                # processed piece square specifications for that move.
                piecesquaregames |= movegames
                piecesquaregames |= piecesquaremovegames
                piecesquaregames ^= piecesquaremovegames
                movegames |= piecesquaregames
                movegames ^= piecesquaregames
                piecesquaremovegames.clear_recordset()
                piecesquaregames.clear_recordset()
            # OR the games found for the position specification on a particular
            # move with the games found on previously processed moves for the
            # position specification
            games |= movegames
            # Do not bother to clear movegames as it is filled with allrecords
            # before next use.
        allgames.close()
        movegames.close()
        piecesquaregames.close()
        piecesquaremovegames.close()
        invertedpiecesquaremovegames.close()
        segmentgames.close()

        # File the list of games under the partial position key.
        if sourceobject is not None:
            self.dbhome.file_records_under(
                self.dbset,
                PARTIALPOSITION_FIELD_DEF,
                games,
                self.dbhome.encode_record_number(sourceobject.key.recno))
            # Remove partial position from set that needs recalculating
            changed = self.dbhome.make_recordset_key(
                PARTIAL_FILE_DEF,
                NEWGAMES_FIELD_DEF,
                key=self.dbhome.encode_record_selector(_NEWGAMES_FIELD_VALUE))
            changed |= ppview
            changed ^= ppview
            self.dbhome.file_records_under(
                PARTIAL_FILE_DEF,
                NEWGAMES_FIELD_DEF,
                changed,
                self.dbhome.encode_record_selector(_NEWGAMES_FIELD_VALUE),
                )
            changed.close()
            ppview.close()

        # Hand the list of games over to the user interface.
        self.set_recordset(games)
