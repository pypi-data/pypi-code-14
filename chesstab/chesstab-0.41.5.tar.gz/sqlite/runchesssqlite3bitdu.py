# runchesssqlite3bitdu.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess database update using custom deferred update for sqlite3.

Run as a new process from the chess GUI.

The customisation is null, and will remain so unless the journals enabling
transaction rollback can be disabled (well then it will not be a customisation
but use of an sqlite3 feature).  DPT deferred update requires that it's
rollback journals are disabled.

"""

if __name__ == '__main__':

    #run by subprocess.popen from ../core/chess.py
    import sys
    import os

    try:
        # If module not loaded from Python site-packages put the folder
        # containing chesstab at front of sys.path on the assumption all the
        # sibling packages are there too.
        try:
            sp = sys.path[-1].replace('\\\\', '\\')
            packageroot = os.path.dirname(
                os.path.dirname(os.path.dirname(__file__)))
            if sp != packageroot:
                sys.path.insert(0, packageroot)
        except NameError as msg:
            # When run in the py2exe generated executable the module will
            # not have the __file__ attribute.
            # But the siblings can be assumed to be in the right place.
            if " '__file__' " not in str(msg):
                raise

        # sys.path should now contain correct chesstab modules
        from chesstab.sqlite import chesssqlite3bitdu
        from chesstab.gui import chessdu

        cdu = chessdu.ChessDeferredUpdate(
            deferred_update_method=chesssqlite3bitdu.chess_sqlite3du,
            database_class=chesssqlite3bitdu.ChessDatabase)
    except:
        try:
            # If chessdu import succeeded write to error log
            chesssqlite3.write_error_to_log()
        except:
            # Assume that parent process will report the failure
            pass
        sys.exit(1)
