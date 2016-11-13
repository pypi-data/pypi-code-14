# sqlite3fullposbit.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""sqlite3 interface to chess database for full position index

List of classes

FullPositionDS - represent subset of games on file that match a postion

"""

from gridsup.apsw.sqlite3bitdatasource import Sqlite3bitDataSource

# Segment... classes imported directly from recordset do not work yet.
#from basesup.dbapi import (SegmentInt, SegmentBitarray, SegmentList)
from basesup.api.database import Recordset
from basesup.api.constants import (
    DB_SEGMENT_SIZE,
    LENGTH_SEGMENT_BITARRAY_REFERENCE,
    LENGTH_SEGMENT_LIST_REFERENCE,
    )

from ..core.filespec import POSITIONS_FIELD_DEF


class FullPositionDS(Sqlite3bitDataSource):
    
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
            self.set_recordset(Recordset(self.dbhome, self.dbset))
            return
            
        recordset = self.dbhome.make_recordset_key(
            self.dbset,
            POSITIONS_FIELD_DEF,
            self.dbhome.encode_record_selector(fullposition))

        self.set_recordset(recordset)
        self.fullposition = fullposition
