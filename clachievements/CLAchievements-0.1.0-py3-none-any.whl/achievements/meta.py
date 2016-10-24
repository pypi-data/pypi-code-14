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

"""'Meta'-achievements"""

from . import Achievement, SimplePersistentDataAchievement
from ..testutils import test_lock, test_unlock

################################################################################

class SoItBegins(Achievement):
    """Get Command Line Achievements up and running."""
    title = "So it begins"

    def __enter__(self):
        self.unlock()

    @staticmethod
    @test_unlock
    def test_single():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls}"

################################################################################

class TheEnd(SimplePersistentDataAchievement):
    """Unlock every achievement."""
    title = "The End"
    default_data = False

    def __enter__(self):
        if self.data:
            self.unlock()

    def __exit__(self, exc_type, exc_value, traceback):
        if len([date for date in self.database.as_dict("status").values() if date is None]) <= 1:
            self.data = True

    @classmethod
    @test_lock
    def test_lock1(cls):
        """Test: iterate over commands that must not unlock this achievement."""
        from ..db import DB
        from ..run import Command
        from . import iter_achievements
        database = DB()
        command = Command(["ls"])
        for achievement in iter_achievements():
            if achievement.__name__ != cls.__name__:
                achievement(command, database).unlock()
        yield "{bin.ls}"

    @classmethod
    @test_unlock
    def test_unlock(cls):
        """Test: iterate over commands that must unlock this achievement."""
        yield from cls.test_lock1()
        yield "{bin.ls}"

################################################################################
