# dptselection.py
# Copyright 2016 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""DPT interface to chess database for selection rules index

List of classes

SelectionDS - represent subset of games on file that match a selection rule.

"""

from dptdb import dptapi

from gridsup.dpt.dptdatasource import DPTDataSource

# Segment... classes imported directly from recordset do not work yet.
#from basesup.dbapi import (SegmentInt, SegmentBitarray, SegmentList)
from basesup.api.database import Recordset


class SelectionDS(DPTDataSource):
    
    """Extend to represent subset of games on file that match a selection rule.

    Methods added:

    get_selection_rule_games - Select games which match selection rule

    Methods overridden:

    None
    
    Methods extended:

    __init__
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        super(SelectionDS, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

    def get_selection_rule_games(self, fullposition):
        """Find game records matching selection rule.

        A Python list and a custom cursor are used to simulate DPT foundset

        """
        gamedb = self.dbhome.get_database(self.dbset, self.dbname)

        # This test copes with databases unavailable while Import in progress.
        # Proper solution awaits implementation of general gridsup support.
        if gamedb is None:
            return

        games = gamedb.CreateRecordList()
        if not fullposition:
            self.set_recordset(games)
            return
        self.set_recordset(fullposition)
