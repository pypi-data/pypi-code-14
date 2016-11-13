# dbfullpos.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""bsddb interface to chess database for full position index

This task can be done much quicker using bsddb cursor directly.  But the bsddb
interface is now about following the DPT interface to ease application problem
fixing rather than being as quick as possible itself.

List of classes

FullPositionDS - represent subset of games on file that match a postion

"""

from gridsup.db.dbdatasource import DBDataSource

from ..core.filespec import POSITIONS_FIELD_DEF


class FullPositionDS(DBDataSource):
    
    """Extend to represent subset of games on file that match a postion.

    Methods added:

    get_full_position_games - Select games which match full position

    Methods overridden:

    None
    
    Methods extended:

    __init__
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Extend to provide placeholder for position used to select games.
        
        Arguments are passed through to superclass

        """
        super(FullPositionDS, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)
        # Position used as key to select games
        self.fullposition = None

    def get_full_position_games(self, fullposition):
        """Find game records matching full position.

        A Python list and a custom cursor are used to simulate DPT foundset

        """
        self.fullposition = None
        if not fullposition:
            self.set_recordset([])
            return

        encodedfullposition = self.dbhome.encode_record_selector(fullposition)
            
        # Ok to use CursorDB._cursor methods because result uses database
        # engine specific methods.  In Berkley DB must simulate an index
        # file with a Python list while DPT uses its list type.
        games = set()
        cursordb = self.dbhome.database_cursor(self.dbset, POSITIONS_FIELD_DEF)
        cursor = cursordb._cursor
        r = cursor.set_range(encodedfullposition)
        while r is not None:
            k, v = r
            if not k.startswith(encodedfullposition):
                break
            games.add(v)
            r = cursor.next()
        cursordb.close()

        cursordb = self.dbhome.database_cursor(self.dbset, self.dbname)
        cursor = cursordb._cursor
        recordset = []
        for g in games:
            r = cursor.set(self.dbhome.decode_as_primary_key(self.dbset, g))
            if r:
                recordset.append(r)
        cursordb.close()
        self.set_recordset(recordset)
        self.fullposition = fullposition
