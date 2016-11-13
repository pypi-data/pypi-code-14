# dptpartpos.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""DPT interface to chess database for partial position index

This module gets a special mention because it is the implementation of the
search in get_partial_position_games() that justifies all the work getting
the C++ code to compile under gcc (thanks to Richard Groves for making the
changes that proved necessary) and building the SWIG interface to allow the
chess application written in Python to get at it.

List of classes

PartialPositionDS - represent subset of games that match a partial postion

"""

from dptdb import dptapi

from gridsup.dpt.dptdatasource import DPTDataSource

from pgn.core.constants import (
    PIECES,
    )

from ..core.constants import (
    MAP_PARTIAL_PIECE_TO_CH,
    MAP_PARTIAL_PIECE_TO_PIECES,
    NULLPIECE,
    PIECE_SQUARE_NOT_ALLOWED,
    )

from ..core.filespec import (
    PIECESQUAREMOVE_FIELD_DEF,
    PARTIAL_FILE_DEF,
    _NEWGAMES_FIELD_NAME,
    _NEWGAMES_FIELD_VALUE,
    _PARTIALPOSITION_FIELD_NAME,
    PARTIALPOSITION_FIELD_DEF,
    )


class PartialPositionDS(DPTDataSource):
    
    """Extend to represent subset of games on file that match a partial postion.

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
        """Find game records matching partial position."""
        gamedb = self.dbhome.get_database(self.dbset, self.dbname)
        # This test copes with databases unavailable while Import in progress.
        # Proper solution awaits implementation of general gridsup support.
        if gamedb is None:
            return
        games = gamedb.CreateRecordList()
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
            partialdb = self.dbhome.get_database(
                PARTIAL_FILE_DEF, PARTIAL_FILE_DEF)
            ppview = partialdb.FindRecords(
                dptapi.APIFindSpecification(
                    dptapi.FD_SINGLEREC,
                    sourceobject.key.recno),
                dptapi.FD_LOCK_SHR)
            pprecalc = partialdb.FindRecords(
                dptapi.APIFindSpecification(
                    _NEWGAMES_FIELD_NAME,
                    dptapi.FD_EQ,
                    dptapi.APIFieldValue(
                        self.dbhome.encode_record_selector(
                            _NEWGAMES_FIELD_VALUE))),
                ppview)
            if pprecalc.Count() == 0:
                ppcalc = gamedb.FindValues(
                    dptapi.APIFindValuesSpecification(
                        self.dbhome.get_dptfiles()[
                            self.dbset]._secondary[PARTIALPOSITION_FIELD_DEF],
                        dptapi.FD_LIKE,
                        dptapi.APIFieldValue(
                            self.dbhome.encode_record_number(
                                sourceobject.key.recno))))
                if ppcalc.Count() != 0:
                    calc = gamedb.FindRecords(
                        dptapi.APIFindSpecification(
                            self.dbhome.get_dptfiles()[
                                self.dbset]._secondary[
                                    PARTIALPOSITION_FIELD_DEF],
                            dptapi.FD_EQ,
                            dptapi.APIFieldValue(
                                self.dbhome.encode_record_number(
                                    sourceobject.key.recno))),
                        dptapi.FD_LOCK_SHR)
                    games.Place(calc)
                    self.set_recordset(games)
                    gamedb.DestroyRecordSet(calc)
                    gamedb.DestroyValueSet(ppcalc)
                    partialdb.DestroyRecordSet(ppview)
                    partialdb.DestroyRecordSet(pprecalc)
                    return
                gamedb.DestroyValueSet(ppcalc)
            partialdb.DestroyRecordSet(pprecalc)

        def DVCursor(piecesquare):
            highkey = ''.join((piecesquare, chr(255))) #key[2] < chr(255)
            return gamedb.OpenDirectValueCursor(
                dptapi.APIFindValuesSpecification(
                    self.dbhome.get_dptfiles()[
                        self.dbset]._secondary[PIECESQUAREMOVE_FIELD_DEF],
                    dptapi.FD_RANGE_GE_LT,
                    dptapi.APIFieldValue(piecesquare),
                    dptapi.APIFieldValue(highkey)),
                dptapi.CURSOR_ASCENDING)

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
            psb = self.dbhome.encode_record_selector(p + chr(square))
            pslen = len(psb)
            cursor = DVCursor(psb)
            while cursor.Accessible():
                v = cursor.GetCurrentValue().ExtractString()
                movepiecesquare.setdefault(
                    v[pslen:], dict()).setdefault(
                        piecesquarebase, []).append(v)
                cursor.Advance(1)
            gamedb.CloseDirectValueCursor(cursor)

        for piecesquare in position:
            square, partialpiece = piecesquare
            pieces = MAP_PARTIAL_PIECE_TO_PIECES.get(
                partialpiece, (partialpiece,))
            for p in pieces:
                if (p, square) in PIECE_SQUARE_NOT_ALLOWED:
                    continue
                psb = self.dbhome.encode_record_selector(p + chr(square))
                pslen = len(psb)
                cursor = DVCursor(psb)
                while cursor.Accessible():
                    v = cursor.GetCurrentValue().ExtractString()
                    move = v[pslen:]
                    if move in movepiecesquare:
                        movepiecesquare[move].setdefault(
                            piecesquare, []).append(v)
                    cursor.Advance(1)
                gamedb.CloseDirectValueCursor(cursor)

        # Find the games using the position specification in movepiecesquare.
        allgames = gamedb.FindRecords()
        movegames = gamedb.CreateRecordList()
        piecesquaregames = gamedb.CreateRecordList()
        piecesquaremovegames = gamedb.CreateRecordList()
        invertedpiecesquaremovegames = gamedb.CreateRecordList()
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
            movegames.Place(allgames)
            for specpiece, psm in moveposition.items():
                for key in psm:
                    pg = gamedb.FindRecords(
                        dptapi.APIFindSpecification(
                            self.dbhome.get_dptfiles()[
                                self.dbset]._secondary[
                                    PIECESQUAREMOVE_FIELD_DEF],
                            dptapi.FD_EQ,
                            dptapi.APIFieldValue(key)),
                        dptapi.FD_LOCK_SHR,
                        allgames)
                    # OR the games found for each piece specified for a square
                    # on a particular move with the games found for previously
                    # processed pieces for that square and move.
                    piecesquaremovegames.Place(pg)
                    gamedb.DestroyRecordSet(pg)
                if specpiece[1] == NULLPIECE:
                    # The square must be empty.
                    # piecesquaremovegames is the games where the square has
                    # a piece so invert the list.
                    invertedpiecesquaremovegames.Place(allgames)
                    invertedpiecesquaremovegames.Remove(piecesquaremovegames)
                    piecesquaremovegames.Clear()
                    piecesquaremovegames.Place(invertedpiecesquaremovegames)
                    # Do not bother to clear invertedpiecesquaremovegames as it
                    # is filled with allrecords before next use.
                # AND the games found for one piece square specification on
                # a particular move with the games found for previously
                # processed piece square specifications for that move.
                piecesquaregames.Place(movegames)
                piecesquaregames.Remove(piecesquaremovegames)
                movegames.Remove(piecesquaregames)
                piecesquaremovegames.Clear()
                piecesquaregames.Clear()
            # OR the games found for the position specification on a particular
            # move with the games found on previously processed moves for the
            # position specification
            games.Place(movegames)
            # Do not bother to clear movegames as it is filled with allrecords
            # before next use.
        gamedb.DestroyRecordSet(allgames)
        gamedb.DestroyRecordSet(movegames)
        gamedb.DestroyRecordSet(piecesquaregames)
        gamedb.DestroyRecordSet(piecesquaremovegames)
        gamedb.DestroyRecordSet(invertedpiecesquaremovegames)

        # File the list of games under the partial position key.
        if sourceobject is not None:
            gamedb.FileRecordsUnder(
                games,
                _PARTIALPOSITION_FIELD_NAME,
                dptapi.APIFieldValue(
                    self.dbhome.encode_record_number(sourceobject.key.recno)))
            # Remove partial position from set that needs recalculating
            rsc = ppview.OpenCursor()
            rsc.GotoFirst()
            while rsc.Accessible():
                r = rsc.AccessCurrentRecordForReadWrite()
                r.DeleteFieldByValue(
                    _NEWGAMES_FIELD_NAME,
                    dptapi.APIFieldValue(
                        self.dbhome.encode_record_selector(
                            _NEWGAMES_FIELD_VALUE)))
                rsc.Advance(1)
            ppview.CloseCursor(rsc)
            self.dbhome.commit()
            partialdb.DestroyRecordSet(ppview)

        # Hand the list of games over to the user interface.
        self.set_recordset(games)
