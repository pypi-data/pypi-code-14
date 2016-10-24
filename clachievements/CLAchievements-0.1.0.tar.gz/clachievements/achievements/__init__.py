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

"""Achievement metaclasses"""

import datetime
import os
import sqlite3

from straight import plugin
import pkg_resources

from clachievements import notify

try:
    from contextlib import AbstractContextManager
except ImportError:
    # This try-block can be removed once python3.5 is deprecated.
    class AbstractContextManager:
        """Abstract class to be subclassed to implement a context manager."""
        # pylint: disable=too-few-public-methods

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return None


class Achievement(AbstractContextManager):
    """Achievement: Something that is unlocked when user perform the right commands.

    A how-to is available in the :ref:`plugin` section, which illustrates this
    class documentation.

    This class is a :ref:`context manager <typecontextmanager>`. The
    :meth:`~contextmanager.__enter__` method is called before the actual
    wrapped command call, and the :meth:`~contextmanager.__exit__` method is
    called after it. One of those method must call :meth:`unlock` when the
    conditions to fulfill the achievement are met.
    """

    #: Title of the achievement. If `None`, the class is an abstract achievement, to be subclassed.
    title = None

    #: List of binaries loading this achievement. If `None`, this achievement is always loaded.
    bin = None

    #: File name of the icon (relative to the data directory).
    icon = "star.svg"

    #: Description of the achievement. If `None`, the first non-empty line
    #: of the class docstring is used instead.
    _description = None

    def __init__(self, command, database):
        super().__init__()

        self.command = command
        self.database = database

        if not self.database.has_key("status", self.keyword):
            try:
                with self.database.conn:
                    self.first()
            except sqlite3.IntegrityError:
                pass

    def first(self):
        """This method is called once: when this achievement is loaded for the first time.

        This method is meant to be subclassed.
        """
        self.database.insert_blob("status", self.keyword, None)

    def last(self):
        """This method is called once: when this achievement has just been unlocked.

        This method is meant to be subclassed.
        """
        pass

    @classmethod
    def description(cls):
        """Return achievement description.

        If :attr:`_description` is defined, return it. Otherwise, return the
        first non-empty line of the docstring.
        """
        if cls._description is not None:
            return cls._description
        try:
            return [line.strip() for line in cls.__doc__.split("\n") if line.strip()][0]
        except (IndexError, AttributeError):
            raise AttributeError("Class '{}' is missing a description.".format(cls.__name__))

    @property
    def keyword(self):
        """Return the name of the class of this achievement."""
        return self.__class__.__name__

    @classmethod
    def match_bin(cls, name):
        """Return `True` iff this achievement is about the given binary."""
        if cls.bin is None:
            return True
        return name in cls.bin # pylint: disable=unsupported-membership-test

    @property
    def fullicon(self):
        """Return absolute path of this achievement icon."""
        return os.path.abspath(
            pkg_resources.resource_filename(
                "clachievements",
                os.path.join("data", "icons", self.icon),
                )
            )

    def unlock(self):
        """Called when achievement is unlocked.

        - Mark this achievement as unlocked in the database.
        - Notify user.

        This method is to be called by one of the :meth:`__enter__` or
        :meth:`__exit__` method when the conditions to unlock the achievement
        are fulfilled.
        """
        while True:
            if not self.database.is_locked(self):
                break
            try:
                with self.database.conn:
                    self.database.update_blob("status", self.keyword, datetime.datetime.now())
                self.last()
            except sqlite3.IntegrityError:
                pass

        if "CLA_TEST" not in os.environ:
            notify.notify(self)

class SimplePersistentDataAchievement(Achievement):
    """Achievement, with a simple way to store data into a database.

    It is very simple to use, since accessing or writing to ``self.data`` will
    automatically read or write data from the database.

    But the cost is that concurrent access to the database *will* lead to
    errors. For instance, on a test, running fifty concurrent calls to
    ``self.data += 1`` only incremented ``self.data`` by about twenty values.

    This is wrong but:

    - this is just a game, so there is no important consequence to this error;
    - this is a very simple class. If you want a more robust one, please
      provide a patch.
    """

    #: Data stored as this achievement persistent data when this
    #: achievement is met for the first time.
    default_data = None

    def first(self):
        """Called to initiate database the first time this achievement is loaded."""
        super().first()
        self.database.insert_blob("data", self.keyword, self.default_data)

    def last(self):
        """Called to clean database, once achievement is unlocked."""
        super().last()
        with self.database.conn:
            self.database.remove_blob("data", self.keyword)

    @property
    def data(self):
        """:mod:`Picklable <pickle>` persistent data, specific to this achievement.

        .. note::

            Database is not locked when reading or writing this data.  That is,
            concurrent runs of ``self.data += 1`` are not guaranteed to succeed.

        .. note::

            Be careful to call ``self.data = MY_NEW_DATA`` to store your
            updated data. This means that, if ``self.data`` is a dictionary,
            ``self.data.update({"foo": "bar"})`` will not store anything.
        """
        return self.database.read_blob("data", self.keyword)

    @data.setter
    def data(self, value):
        try:
            with self.database.conn:
                self.database.update_blob("data", self.keyword, value)
        except sqlite3.IntegrityError:
            # This is a *very* simple engine. For more complex (and
            # correct) uses, write it yourself.
            pass

def iter_achievements():
    """Iterator over the achievements."""
    for achievement in set(plugin.load('clachievements.achievements', subclasses=Achievement)):
        if achievement.title is not None:
            yield achievement
