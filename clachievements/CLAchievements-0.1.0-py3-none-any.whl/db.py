# Command Line Achievements
# Copyright 2016 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Management of databases"""

from tempfile import mkdtemp
import os
import pickle
import shutil
import sqlite3

from xdg.BaseDirectory import xdg_data_home

ENV_DBPATH = "CLA_DBPATH"
DB_VERSION = 1

def db_path():
    """Return the path of the sqlite file.

    If the environment variable ``ENV_DBPATH`` is defined, return its
    value; otherwise, return a default value.
    """
    return os.path.join(
        os.environ.get(
            ENV_DBPATH,
            os.path.join(xdg_data_home, "clachievements"),
            ),
        "achievements.db",
        )

class DB:
    """Database storing information about achievement progress.

    Tables `status` and `data` are dict-like tables, where arbitrary
    values (any picklable object) are associated with keys (which must be
    strings). All the methods of this class consider that the table given
    in arguments is such a kind of tables.
    """

    def __init__(self):
        if not os.path.exists(db_path()):
            os.makedirs(os.path.dirname(db_path()), exist_ok=True)
            try:
                with sqlite3.connect(db_path()) as conn:
                    conn.execute("CREATE TABLE status (key TEXT PRIMARY KEY, value BLOB)")
                    conn.execute("CREATE TABLE data (key TEXT PRIMARY KEY, value BLOB)")
                    conn.execute("CREATE TABLE version (key INTEGER PRIMARY KEY)")
                    conn.execute("INSERT INTO version VALUES (?)", (DB_VERSION, ))
            except sqlite3.IntegrityError:
                # Database have been created by another process
                pass

        self.conn = sqlite3.connect(db_path())
        self.conn.execute("PRAGMA busy_timeout = 30000")

    def read_blob(self, table, key):
        """Return the value associated to the key, in the table.

        Since the table behave like a dictionary, this is similar to
        ``table[key]``.
        """
        row = self.conn.execute(
            'SELECT value FROM {} WHERE key=?'.format(table), (key, )
            ).fetchone()
        if row is None:
            raise KeyError("No key '{}' in table '{}'.".format(key, table))
        return pickle.loads(row[0])

    def insert_blob(self, table, key, value):
        """Insert the key in the table.

        Since this table can be considered as a dictionary, this is
        similar to the pseudo-code ``table[key] = value``, if the key does
        not appear yet in the table.
        """
        self.conn.execute(
            'INSERT INTO {} VALUES (?, ?)'.format(table), (key, pickle.dumps(value))
        )

    def update_blob(self, table, key, value):
        """Update the key in the table.

        Since this table can be considered as a dictionary, this is
        similar to the pseudo-code ``table[key] = value`` if the key is
        already present in the table.

        The transaction is not commited. You must enclose any call to this
        method in the connection :attr:`self.conn` considered as a context
        manager, or call ``self.conn.commit()`` afterward.
        """
        self.conn.execute(
            'UPDATE {} SET value=? WHERE key=?'.format(table), (pickle.dumps(value), key)
        )

    def remove_blob(self, table, key):
        """Remove key from table.

        Since this table can be considered as a dictionary, this is
        similar to the pseudo-code ``del table[key]``.

        The transaction is not commited. You must enclose any call to this
        method in the connection :attr:`self.conn` considered as a context
        manager, or call ``self.conn.commit()`` afterward.
        """
        self.conn.execute(
            'DELETE FROM {} WHERE key=?'.format(table), (key, )
        )

    def as_dict(self, table):
        """Return the table as a :class:`dict`."""
        return {
            key[0]: self.read_blob(table, key[0])
            for key
            in self.conn.execute('SELECT key FROM {}'.format(table)).fetchall()
            }

    def is_locked(self, achievement):
        """Return `True` iff achievement is locked.

        Achievement can be either a (sub)class or an instance of the
        :class:`achievement.Achievement` class.
        """
        if isinstance(achievement, type):
            keyword = achievement.__name__
        else:
            keyword = achievement.__class__.__name__
        try:
            return self.read_blob("status", keyword) is None
        except KeyError:
            return True

    def has_key(self, table, key):
        """Return `True` iff table has an entry with the given key."""
        return self.conn.execute(
            'SELECT value FROM {} WHERE key=?'.format(table), (key,)
            ).fetchone() is not None

    def unlock_date(self, achievement):
        """Return unlock date, or `None` if achievement is locked."""
        try:
            return self.read_blob("status", achievement.__name__)
        except KeyError:
            return None

class TempDB:
    """Context manager to open a temporary database.

    Any new :class:`DB` object withing this scope will use this database.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self._tempdir = None
        self._olddir = None

    def __enter__(self):
        self._tempdir = mkdtemp()
        self._olddir = os.environ.get("CLA_DBPATH", None)
        os.environ["CLA_DBPATH"] = self._tempdir
        return DB(*self.args, **self.kwargs)

    def __exit__(self, *args, **kwargs):
        shutil.rmtree(self._tempdir, ignore_errors=True)
        if self._olddir is None:
            del os.environ["CLA_DBPATH"]
        else:
            os.environ["CLA_DBPATH"] = self._olddir
