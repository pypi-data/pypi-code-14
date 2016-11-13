# chesssqlite3bitdu.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess database update using custom deferred update for sqlite3.

List of classes

ChessDatabase - chess database in custom deferred update mode.

List of functions

chess_sqlite3du - import games from *.pgn files to database

"""

import os
import bz2
import subprocess
import sys
import base64

from basesup.apswduapi import Sqlite3bitduapi, Sqlite3duapiError
from basesup.api.constants import FILEDESC, DB_SEGMENT_SIZE

from ..core.filespec import (
    FileSpec,
    GAMES_FILE_DEF,
    )
from ..core.chessrecord import ChessDBrecordGameImport

_platform_win32 = sys.platform == 'win32'
_python_version = '.'.join(
    (str(sys.version_info[0]),
     str(sys.version_info[1])))


def chess_sqlite3du(
    dbpath,
    pgnpaths,
    file_records,
    reporter=lambda text, timestamp=True: None):
    """Open database, import games and close database."""
    cdb = ChessDatabase(dbpath, allowcreate=True)
    importer = ChessDBrecordGameImport()
    if cdb.open_context():
        cdb.set_defer_update(db=GAMES_FILE_DEF)
        for pp in pgnpaths:
            s = open(pp, 'r', encoding='iso-8859-1')
            importer.import_pgn(cdb, s, pp, reporter=reporter)
            s.close()
        if reporter is not None:
            reporter('Finishing import: please wait.')
            reporter('', timestamp=False)
        cdb.do_deferred_updates(db=GAMES_FILE_DEF)
        cdb.unset_defer_update(db=GAMES_FILE_DEF)
    cdb.close_context()

    # There are no recoverable file full conditions for sqlite3 (see DPT).
    return True


class ChessDatabase(Sqlite3bitduapi):

    """Provide custom deferred update for a database of games of chess.

    Methods added:

    add_import_buttons
    archive
    delete_archive
    get_archive_names
    get_file_sizes
    open_context_prepare_import
    report_plans_for_estimate

    Methods overridden:

    None
    
    Methods extended:

    __init__
    
    """
    # Assuming 2Gb memory:
    # A default FreeBSD user process will not cause the MemoryError exception,
    # selecting the optimum chunk size, 65536 games, defined in the superclass.
    # A MS Windows XP process will cause the MemoryError exeption which selects
    # the 32768 game chunk size.
    # A default OpenBSD user process will cause the MemoryError exception which
    # selects the 16384 game chunk size.
    for f, m in ((4, 700000000), (2, 1400000000)):
        try:
            b' ' * m
        except MemoryError:
            deferred_update_points = frozenset(
                [i for i in range(DB_SEGMENT_SIZE//f-1,
                                  DB_SEGMENT_SIZE,
                                  DB_SEGMENT_SIZE//f)])
            break
    del f, m

    def __init__(self, sqlite3file, **kargs):
        """Define chess database.

        **kargs
        allowcreate == False - remove file descriptions from FileSpec so
        that superclass cannot create them.
        Other arguments are passed through to superclass __init__.
        
        """
        names = FileSpec(**kargs)

        if not kargs.get('allowcreate', False):
            try:
                for t in names:
                    if FILEDESC in names[t]:
                        del names[t][FILEDESC]
            except:
                if __name__ == '__main__':
                    raise
                else:
                    raise Sqlite3duapiError('sqlite3 description invalid')

        try:
            super(ChessDatabase, self).__init__(
                names,
                sqlite3file,
                **kargs)
        except Sqlite3duapiError:
            if __name__ == '__main__':
                raise
            else:
                raise Sqlite3duapiError('sqlite3 description invalid')
    
    def open_context_prepare_import(self):
        """Return True

        No preparation actions thet need database open for sqlite3.

        """
        #return super(ChessDatabaseDeferred, self).open_context()
        return True
    
    def get_archive_names(self, files=()):
        """Return sqlite3 database file and existing operating system files"""
        names = [self.get_database_filename()]
        exists = [os.path.basename(n)
                  for n in names if os.path.exists('.'.join((n, 'bz2')))]
        return (names, exists)

    def archive(self, flag=None, names=None):
        """Write a bz2 backup of file containing games.

        Intended to be a backup in case import fails.

        """
        if names is None:
            return False
        if not self.delete_archive(flag=flag, names=names):
            return
        if flag:
            for n in names:
                c = bz2.BZ2Compressor()
                archiveguard = '.'.join((n, 'grd'))
                archivename = '.'.join((n, 'bz2'))
                fi = open(n, 'rb')
                fo = open(archivename, 'wb')
                inp = fi.read(10000000)
                while inp:
                    co = c.compress(inp)
                    if co:
                        fo.write(co)
                    inp = fi.read(10000000)
                co = c.flush()
                if co:
                    fo.write(co)
                fo.close()
                fi.close()
                c = open(archiveguard, 'wb')
                c.close()
        return True

    def delete_archive(self, flag=None, names=None):
        """Delete a bz2 backup of file containing games."""
        if names is None:
            return False
        if flag:
            for n in names:
                archiveguard = '.'.join((n, 'grd'))
                archivename = '.'.join((n, 'bz2'))
                try:
                    os.remove(archiveguard)
                except:
                    pass
                try:
                    os.remove(archivename)
                except:
                    pass
        return True

    def add_import_buttons(self, *a):
        """Add button actions for Berkeley DB to Import dialogue.

        None required.  Method exists for DPT compatibility.

        """
        pass

    def get_file_sizes(self):
        """Return an empty dictionary.

        No sizes needed.  Method exists for DPT compatibility.

        """
        return dict()

    def report_plans_for_estimate(self, estimates, reporter):
        """Remind user to check estimated time to do import.

        No planning needed.  Method exists for DPT compatibility.

        """
        # See comment near end of class definition Chess in relative module
        # ..gui.chess for explanation of this change.
        #reporter.append_text_only(''.join(
        #    ('The expected duration of the import may make starting ',
        #     'it now inconvenient.',
        #     )))
        #reporter.append_text_only('')
